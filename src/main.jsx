import React, { useCallback, useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

const QUEUE_KEY = "astrovital_demo_queue";
const OFFLINE_KEY = "astrovital_demo_offline";
const DEMO_ROLES = [
  { username: "alex.demo", name: "Alex Demo", detail: "Astronaut portal · view profile, check in, follow up" },
  { username: "doctor.demo", name: "Dr. Maya Chen", detail: "Flight surgeon · review cases, analyze trends, recommend" },
  { username: "admin.demo", name: "Mission Admin", detail: "Administrator · technical audit and demo reset" },
];

function readQueue() {
  try {
    const queue = JSON.parse(localStorage.getItem(QUEUE_KEY) || "[]");
    return Array.isArray(queue) ? queue : [];
  } catch {
    return [];
  }
}

function formatTime(value) {
  if (!value) return "Time not recorded";
  return new Intl.DateTimeFormat("en", {
    month: "short", day: "numeric", hour: "2-digit", minute: "2-digit",
  }).format(new Date(value));
}

function titleCase(value = "") {
  return value.replaceAll("_", " ").replace(/\b\w/g, (letter) => letter.toUpperCase());
}

async function api(url, options = {}) {
  const response = await fetch(url, {
    ...options,
    credentials: "include",
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
  });
  const payload = await response.json();
  if (!response.ok) {
    const detail = payload.detail;
    throw new Error(typeof detail === "string" ? detail : detail?.message || payload.error?.message || "The request failed.");
  }
  return payload;
}

function App() {
  const [user, setUser] = useState(null);
  const [data, setData] = useState(null);
  const [view, setView] = useState("overview");
  const [selectedCaseId, setSelectedCaseId] = useState(null);
  const [offline, setOffline] = useState(localStorage.getItem(OFFLINE_KEY) === "true");
  const [queue, setQueue] = useState(readQueue);
  const [toast, setToast] = useState("");
  const [loading, setLoading] = useState(true);
  const [working, setWorking] = useState(false);

  const notify = useCallback((message) => {
    setToast(message);
    window.setTimeout(() => setToast(""), 3500);
  }, []);

  const refresh = useCallback(async () => {
    const result = await api("/api/dashboard");
    setData(result);
    setQueue(readQueue());
    return result;
  }, []);

  const syncQueue = useCallback(async (force = false) => {
    const pending = readQueue();
    if ((offline && !force) || !pending.length) return;
    const result = await api("/api/sync/check-ins", {
      method: "POST",
      body: JSON.stringify({ items: pending.slice(0, 10) }),
    });
    const confirmed = new Set(result.results.map((item) => item.clientSubmissionId));
    const remaining = pending.filter((item) => !confirmed.has(item.client_submission_id));
    localStorage.setItem(QUEUE_KEY, JSON.stringify(remaining));
    setQueue(remaining);
    if (result.results.length) notify(`${result.results.length} queued check-in(s) confirmed received by the demo service.`);
  }, [offline, notify]);

  useEffect(() => {
    let active = true;
    (async () => {
      try {
        const session = await api("/api/me");
        if (!active || !session.user) return;
        setUser(session.user);
        let result = await api("/api/dashboard");
        if (active) setData(result);
        if (session.user.role === "astronaut" && !offline) {
          await syncQueue(true);
          result = await api("/api/dashboard");
          if (active) setData(result);
        }
      } catch (error) {
        if (active) notify(error.message);
      } finally {
        if (active) setLoading(false);
      }
    })();
    return () => { active = false; };
  }, [notify, offline, syncQueue]);

  const cases = data?.cases || [];
  const selectedCase = useMemo(
    () => cases.find((item) => item.id === selectedCaseId) || cases[0] || null,
    [cases, selectedCaseId],
  );

  async function signIn(username) {
    setWorking(true);
    try {
      const result = await api("/api/login", { method: "POST", body: JSON.stringify({ username }) });
      setUser(result.user);
      setView(result.user.role === "admin" ? "audit" : "overview");
      const dashboard = await api("/api/dashboard");
      setData(dashboard);
      if (result.user.role === "astronaut" && !offline) {
        await syncQueue(true);
        setData(await api("/api/dashboard"));
      }
      notify(`Demo session started as ${result.user.name}.`);
    } catch (error) {
      notify(error.message);
    } finally {
      setLoading(false);
      setWorking(false);
    }
  }

  async function signOut() {
    await api("/api/logout", { method: "POST", body: "{}" });
    setUser(null);
    setData(null);
    setView("overview");
    setSelectedCaseId(null);
  }

  async function toggleOffline(event) {
    const next = event.target.checked;
    setOffline(next);
    localStorage.setItem(OFFLINE_KEY, String(next));
    if (!next) {
      try {
        await syncQueue(true);
        await refresh();
      } catch (error) {
        notify(`Reconnect could not be confirmed: ${error.message}`);
      }
    } else {
      notify("Offline simulation on. New check-ins are queued locally, not delivered.");
    }
  }

  async function submitCheckIn(formData) {
    const item = {
      client_submission_id: crypto.randomUUID(),
      symptoms: formData.getAll("symptoms"),
      severity: Number(formData.get("severity")),
      trend: formData.get("trend"),
      description: formData.get("description"),
    };
    if (!item.symptoms.length) throw new Error("Select at least one symptom.");
    if (!item.severity || !item.trend) throw new Error("Choose severity and a trend.");
    if (offline) {
      const pending = [...readQueue(), item];
      localStorage.setItem(QUEUE_KEY, JSON.stringify(pending));
      setQueue(pending);
      setView("overview");
      notify("Saved in this browser: queued locally, not delivered to the medical team.");
      return;
    }
    await api("/api/check-ins", { method: "POST", body: JSON.stringify(item) });
    await refresh();
    setView("overview");
    notify("Check-in received by the demo service and added to the clinician case queue.");
  }

  async function runAction(action) {
    setWorking(true);
    try {
      await action();
    } catch (error) {
      notify(error.message);
    } finally {
      setWorking(false);
    }
  }

  if (loading) return <div className="boot-screen">Loading mission workspace…</div>;
  if (!user) return <Login onLogin={signIn} working={working} toast={toast} />;

  const nav = user.role === "astronaut"
    ? [["overview", "Mission overview"], ["check-in", "Symptom check-in"], ["recommendations", "Care follow-up"]]
    : user.role === "flight_surgeon"
      ? [["overview", "Mission overview"], ["cases", "Case review"]]
      : [["audit", "System overview"]];

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <Brand />
        <div className="side-label">{user.role === "astronaut" ? "Crew portal" : user.role === "flight_surgeon" ? "Medical operations" : "Administration"}</div>
        <nav>{nav.map(([key, label]) => (
          <button key={key} className={`nav-item ${view === key ? "active" : ""}`} onClick={() => setView(key)}>{label}</button>
        ))}</nav>
        <div className="sidebar-bottom">
          <div className="role-card"><div className="avatar">{user.name.split(" ").map((word) => word[0]).slice(0, 2).join("")}</div><div><strong>{user.name}</strong><small>{titleCase(user.role)}</small></div></div>
          <button className="logout" onClick={() => runAction(signOut)}>↗ &nbsp; Sign out of demo</button>
        </div>
      </aside>
      <main className="main-area">
        <header className="topbar">
          <div className="breadcrumb">ASTROVITAL X <span>/</span> {titleCase(view)}</div>
          <div className="top-actions">
            <div className="sync-state"><span className={`dot ${offline ? "amber-dot" : ""}`} />{offline ? "Offline simulation" : "Connected"} <span>·</span> last sync {formatTime(data?.lastSyncAt)}</div>
            <label className="toggle-wrap" title="Simulates an unavailable service link">
              <input className="switch" type="checkbox" checked={offline} onChange={toggleOffline} aria-label="Toggle offline simulation" />
              Offline
            </label>
            <button className="logout-mobile" onClick={() => runAction(signOut)}>Sign out</button>
          </div>
        </header>
        <div className="content">
          <div className={`sim-banner ${offline ? "offline" : ""}`}>
            <div><strong>SIMULATED DATA — NOT FOR MEDICAL USE</strong><div>Fictional demo records only · not a measurement, diagnosis, or live spacecraft connection</div></div>
            <span>{queue.length ? `${queue.length} queued locally — not delivered` : offline ? "Items saved now will be queued, not delivered." : "No live spacecraft, agency, or sensor connection."}</span>
          </div>
          {user.role === "admin" ? (
            <AdminView data={data} onReset={() => runAction(async () => {
              await api("/api/demo/reset", { method: "POST", body: "{}" });
              localStorage.removeItem(QUEUE_KEY);
              localStorage.setItem(OFFLINE_KEY, "false");
              setQueue([]);
              setOffline(false);
              await refresh();
              notify("Synthetic demo records reset.");
            })} />
          ) : view === "check-in" ? (
            <CheckInView working={working} onSubmit={(form) => runAction(() => submitCheckIn(new FormData(form)))} />
          ) : user.role === "astronaut" && view === "recommendations" ? (
            <RecommendationsView cases={cases} working={working} onAcknowledge={(id) => runAction(async () => {
              await api(`/api/recommendations/${id}/acknowledgement`, { method: "POST", body: "{}" });
              await refresh();
              notify("Acknowledgement recorded.");
            })} onFollowUp={(id, content) => runAction(async () => {
              await api(`/api/recommendations/${id}/follow-up`, { method: "POST", body: JSON.stringify({ content }) });
              await refresh();
              notify("Follow-up response submitted to the case.");
            })} />
          ) : user.role === "flight_surgeon" && view === "cases" ? (
            <CaseQueue cases={cases} onSelect={(id) => { setSelectedCaseId(id); setView("case-detail"); }} onBack={() => setView("overview")} />
          ) : user.role === "flight_surgeon" && view === "case-detail" ? (
            <CaseDetail
              item={selectedCase}
              working={working}
              onBack={() => setView("cases")}
              onDisposition={(alert, action) => runAction(async () => {
                let reason = "";
                if (action !== "acknowledged") {
                  reason = window.prompt(`Reason to ${action}:`, "");
                  if (reason === null) return;
                }
                await api(`/api/alerts/${alert.id}/disposition`, {
                  method: "POST",
                  body: JSON.stringify({ action, reason }),
                });
                await refresh();
                notify("Alert disposition recorded.");
              })}
              onRecommend={(form) => runAction(async () => {
                const values = new FormData(form);
                await api("/api/recommendations", {
                  method: "POST",
                  body: JSON.stringify({
                    case_id: values.get("case_id"),
                    recommendation_type: values.get("recommendation_type"),
                    content: values.get("content"),
                    follow_up_due_at: values.get("follow_up_due_at") || null,
                  }),
                });
                await refresh();
                notify("Clinician-authored follow-up sent to the astronaut portal.");
              })}
            />
          ) : (
            <Overview
              user={user}
              data={data}
              cases={cases}
              queue={queue}
              onNewCheckIn={() => setView("check-in")}
              onOpenCases={() => setView("cases")}
              onSelectCase={(id) => { setSelectedCaseId(id); setView("case-detail"); }}
              onAcknowledge={(id) => runAction(async () => {
                await api(`/api/recommendations/${id}/acknowledgement`, { method: "POST", body: "{}" });
                await refresh();
                notify("Acknowledgement recorded and added to the audit trail.");
              })}
              onAnalyze={() => runAction(async () => {
                const result = await api("/api/analysis/evaluate", { method: "POST", body: "{}" });
                await refresh();
                notify(result.status === "completed" ? "Demo analysis completed; source-linked flag is ready for clinician review." : "Insufficient synthetic heart-rate history for this demo rule.");
              })}
            />
          )}
        </div>
      </main>
      {toast && <div className="toast" role="status">{toast}</div>}
    </div>
  );
}

function Brand() {
  return <div className="brand-lockup"><div className="brand-mark">A</div><div>ASTROVITAL X<small>MISSION HEALTH</small></div></div>;
}

function Login({ onLogin, working, toast }) {
  return (
    <main className="login-screen">
      <div className="login-wrap">
        <section className="login-copy">
          <Brand />
          <div className="eyebrow login-eyebrow">A connected care concept</div>
          <h1>Health, with a <span>clearer</span> line home.</h1>
          <p>One shared workspace for astronaut check-ins, health context and clinician follow-up — designed for when the signal is strong, and when it is not.</p>
          <div className="login-points"><span>Source-linked records and transparent demo rules</span><span>Ground medical review stays human-led</span><span>Queued states never pretend to be delivered</span></div>
        </section>
        <section className="login-panel">
          <div className="eyebrow">Demo environment</div><h2>Enter the mission workspace</h2>
          <p>Choose a synthetic demo role. No password or external service required.</p>
          {DEMO_ROLES.map((role) => <button key={role.username} className="role-choice" disabled={working} onClick={() => onLogin(role.username)}><strong>{role.name}</strong><small>{role.detail}</small></button>)}
          <div className="safety-note">Prototype access only. All displayed health information is synthetic. This software does not measure vital signs, provide emergency response, diagnose, or prescribe.</div>
          {toast && <div className="toast-inline" role="status">{toast}</div>}
        </section>
      </div>
    </main>
  );
}

function Heading({ kicker, title, description, children }) {
  return <div className="page-heading"><div><div className="eyebrow">{kicker}</div><h1>{title}</h1><p>{description}</p></div>{children}</div>;
}

function Metric({ label, value, unit, detail, icon }) {
  return <div className="metric-card"><div className="metric-top">{label}<span className="metric-icon">{icon}</span></div><div className="metric-value">{value} <small>{unit}</small></div><div className="metric-foot">{detail}</div></div>;
}

function HeartRateChart({ observations = [] }) {
  const points = observations.filter((item) => item.dataType === "heart_rate" && item.value != null);
  if (points.length < 2) return <div className="empty-state">Not enough synthetic history to draw a trend.</div>;
  const values = points.map((point) => Number(point.value));
  const width = 620, height = 190, pad = { left: 36, right: 12, top: 15, bottom: 26 };
  const min = Math.min(...values) - 5, max = Math.max(...values) + 5;
  const x = (index) => pad.left + index * (width - pad.left - pad.right) / (values.length - 1);
  const y = (value) => pad.top + (max - value) * (height - pad.top - pad.bottom) / (max - min);
  const line = values.map((value, index) => `${index ? "L" : "M"} ${x(index)} ${y(value)}`).join(" ");
  const area = `${line} L ${x(values.length - 1)} ${height - pad.bottom} L ${x(0)} ${height - pad.bottom} Z`;
  const ticks = [Math.round(min / 10) * 10, Math.round((min + max) / 20) * 10, Math.round(max / 10) * 10];
  return (
    <>
      <svg className="chart" viewBox={`0 0 ${width} ${height}`} role="img" aria-label="Synthetic heart-rate history; final two samples are demo-rule evidence">
        <defs><linearGradient id="chartFill" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stopColor="#4ed8c3" stopOpacity=".2" /><stop offset="1" stopColor="#4ed8c3" stopOpacity="0" /></linearGradient></defs>
        {ticks.map((tick) => <g key={tick}><line className="chart-grid" x1={pad.left} y1={y(tick)} x2={width - pad.right} y2={y(tick)} /><text className="chart-label" x="0" y={y(tick) + 3}>{tick}</text></g>)}
        <path className="chart-area" d={area} /><path className="chart-line" d={line} />
        {values.map((value, index) => <circle key={points[index].id} className={`chart-point ${index >= values.length - 2 ? "flagged" : ""}`} cx={x(index)} cy={y(value)} r="4"><title>{points[index].id}: {value} {points[index].unit} · synthetic</title></circle>)}
        <text className="chart-label" x={pad.left} y={height - 4}>Earlier</text><text className="chart-label" x={width - pad.right - 42} y={height - 4}>Latest</text>
      </svg>
      <div className="legend"><span className="legend-line" /> Synthetic heart rate <span className="pill amber">demo rule evidence</span></div>
    </>
  );
}

function Overview({ user, data, cases, queue, onNewCheckIn, onOpenCases, onSelectCase, onAcknowledge, onAnalyze }) {
  const observations = data?.observations || [];
  const latest = (key) => [...observations].reverse().find((item) => item.dataType === key);
  const openAlerts = cases.flatMap((item) => item.alerts || []).filter((item) => item.status === "new");
  const recent = (key) => latest(key) || {};
  const recommendations = cases.flatMap((item) => item.recommendations || []);
  const isAstronaut = user.role === "astronaut";
  return (
    <>
      <Heading kicker={isAstronaut ? "Crew health snapshot" : "Mission medical operations"} title={isAstronaut ? `Good morning, ${data?.profile?.name || "Alex"}` : "Crew overview"} description={isAstronaut ? `${data?.profile?.mission || "Expedition Demo"} · synthetic profile · latest available information and next steps.` : "Assigned crew, current review items and data freshness."}>
        {isAstronaut ? <button className="btn primary" onClick={onNewCheckIn}>＋ &nbsp; New check-in</button> : <button className="btn" onClick={onOpenCases}>Open case queue &nbsp; →</button>}
      </Heading>
      <div className="metrics">
        <Metric label="Heart rate" value={recent("heart_rate").value ?? "—"} unit="beats/min" detail="Latest synthetic sample" icon="↗" />
        <Metric label="SpO2" value={recent("spo2").value ?? "—"} unit="%" detail="Latest synthetic sample" icon="◌" />
        <Metric label="Sleep duration" value={recent("sleep_duration").value ?? "—"} unit="hours" detail="Synthetic demo log" icon="◷" />
        <Metric label="Open cases" value={cases.filter((item) => item.status !== "closed").length} unit="cases" detail={`${openAlerts.length} open demo flags`} icon="⌁" />
      </div>
      {user.role === "flight_surgeon" && (
        <section className="card analysis-control">
          <div><h2>AI health analysis</h2><p>Deterministic, explainable demo rule · synthetic samples only · clinician review required</p></div>
          <button className="btn primary" onClick={onAnalyze}>Run demo analysis</button>
        </section>
      )}
      <div className="layout-grid">
        <div>
          <section className="card">
            <div className="card-heading"><div><h2>Health timeline</h2><p>Heart rate · synthetic data · source: Synthetic demo feed</p></div><span className="pill teal">{observations.filter((item) => item.dataType === "heart_rate").length} records</span></div>
            <HeartRateChart observations={observations} />
          </section>
          <section className="card">
            <div className="card-heading"><div><h2>Latest observations</h2><p>Source, timestamp, unit and quality shown</p></div><span className="pill">Synthetic</span></div>
            <div className="observation-list">
              {["heart_rate", "spo2", "sleep_duration", "blood_pressure"].map((key) => {
                const item = recent(key);
                return item.id ? <div className="observation" key={key}><div><strong>{titleCase(item.dataType)}</strong><small>{item.source} · {formatTime(item.observedAt)} · {titleCase(item.quality)}</small></div><div className="obs-value">{item.value} <small>{item.unit}</small></div></div> : null;
              })}
            </div>
          </section>
          {isAstronaut && queue.length > 0 && <QueueCard queue={queue} />}
          {!isAstronaut && <CaseQueue cases={cases} onSelect={onSelectCase} compact />}
        </div>
        <div>
          <section className="card">
            <div className="card-heading"><div><h2>Review signals</h2><p>Software flags are not diagnoses</p></div><span className={`pill ${openAlerts.length ? "amber" : "teal"}`}>{openAlerts.length} open</span></div>
            {openAlerts.length ? openAlerts.slice(0, 2).map((alert) => <div className="rule-card" key={alert.id}><h3>{alert.title}</h3><p>{alert.explanation}</p><div className="rule-meta"><span>{alert.ruleVersion}</span><span>{alert.evidenceIds.length} linked records</span></div></div>) : <div className="empty-state">No unacknowledged demo flags. This does not imply a health assessment.</div>}
            {cases[0] && <div className="recent-case"><p className="section-label">Recent case</p><button className="case-row" onClick={() => isAstronaut ? null : onSelectCase(cases[0].id)}><div><strong>{cases[0].title}</strong><small>{formatTime(cases[0].createdAt)} · {cases[0].checkIn ? "Symptom check-in received" : "Seeded synthetic scenario"}</small></div><span className={`pill ${cases[0].status === "new" ? "amber" : "blue"}`}>{titleCase(cases[0].status)}</span></button></div>}
            <div className="disclaimer">Deterministic demo-only logic using fictional inputs. Not a medical threshold or validated prediction.</div>
          </section>
          <section className="card">
            <div className="card-heading"><div><h2>{isAstronaut ? "Care follow-up" : "Recent clinician actions"}</h2><p>{isAstronaut ? "Clinician-authored guidance" : "Clinician-authored and timestamped"}</p></div></div>
            {recommendations.length ? recommendations.slice(0, 2).map((recommendation) => <div className="recommendation" key={recommendation.id}><span className={`pill ${recommendation.status === "acknowledged" ? "teal" : "blue"}`}>{titleCase(recommendation.status)}</span><p>{recommendation.content}</p><small>By {recommendation.authorName} · {formatTime(recommendation.createdAt)}</small>{isAstronaut && recommendation.status === "sent" && <button className="btn primary ack-button" onClick={() => onAcknowledge(recommendation.id)}>Acknowledge</button>}</div>) : <div className="empty-state">No clinician recommendation yet.</div>}
          </section>
        </div>
      </div>
    </>
  );
}

function QueueCard({ queue }) {
  return <section className="card"><div className="card-heading"><div><h2>Waiting to sync</h2><p>Medical team has not received these entries</p></div><span className="pill amber">{queue.length} queued</span></div>
    {queue.map((item) => <div className="event-row" key={item.client_submission_id}><span className="event-dot amber-background" /><div><strong>Symptom check-in · {item.symptoms.join(", ")}</strong><small>Queued locally · not delivered</small></div></div>)}
    <div className="disclaimer">Saved to this browser only. Not delivered, viewed, or acknowledged. Reconnect to sync.</div>
  </section>;
}

function CaseQueue({ cases, onSelect, compact = false, onBack }) {
  return <section className={`card ${compact ? "case-queue-compact" : ""}`}>
    <div className="card-heading"><div><h2>{compact ? "Assigned cases" : "Case queue"}</h2><p>{cases.length} synthetic case(s) · assigned access</p></div>{onBack && <button className="btn subtle" onClick={onBack}>← All cases</button>}</div>
    <div className="case-list">{cases.length ? cases.map((item) => <button className="case-row" key={item.id} onClick={() => onSelect(item.id)}><div><strong>{item.title}</strong><small>{formatTime(item.createdAt)} · {item.checkIn ? `${item.checkIn.symptoms.join(", ")} · self-reported ${item.checkIn.severity}/5` : "Synthetic demo scenario"}</small></div><span className={`pill ${item.status === "new" ? "amber" : "blue"}`}>{titleCase(item.status)}</span></button>) : <div className="empty-state">No cases assigned.</div>}</div>
  </section>;
}

function CaseDetail({ item, onBack, onDisposition, onRecommend, working }) {
  if (!item) return <><Heading kicker="Case review" title="No assigned cases" description="New astronaut check-ins will appear here." /><div className="card empty-state">There are no cases to review.</div></>;
  return <>
    <Heading kicker="Clinical review" title={item.title} description={`Alex Demo · ${formatTime(item.createdAt)} · ${titleCase(item.priority)} review`}>
      <button className="btn subtle" onClick={onBack}>← &nbsp; All cases</button>
    </Heading>
    <div className="detail-grid">
      <div>
        {item.checkIn && <section className="card"><div className="card-heading"><div><h2>Astronaut check-in</h2><p>Self-reported · {formatTime(item.checkIn.submittedAt)}</p></div><span className="pill teal">Synthetic</span></div><p><strong>Reported:</strong> {item.checkIn.symptoms.join(", ")}</p><p className="muted small">Severity {item.checkIn.severity}/5 · trend {item.checkIn.trend}{item.checkIn.description && <><br />{item.checkIn.description}</>}</p></section>}
        <section className="card"><div className="card-heading"><div><h2>Alert analysis</h2><p>Source-linked finding · demo-only rule version</p></div></div>
          {item.alerts.length ? item.alerts.map((alert) => <div className="flag-box" key={alert.id}><span className={`pill ${alert.status === "new" ? "amber" : "teal"}`}>{titleCase(alert.status)}</span><h3>{alert.title}</h3><p>{alert.explanation}</p><div className="rule-meta"><span>{alert.ruleVersion}</span><span>{alert.evidenceIds.length} evidence IDs: {alert.evidenceIds.join(", ")}</span></div>{alert.dispositionReason && <p className="disposition-reason"><strong>Disposition:</strong> {alert.dispositionReason}</p>}{alert.status === "new" && <div className="case-actions"><button disabled={working} className="btn primary" onClick={() => onDisposition(alert, "acknowledged")}>Acknowledge</button><button disabled={working} className="btn subtle" onClick={() => onDisposition(alert, "dismissed")}>Dismiss</button><button disabled={working} className="btn subtle" onClick={() => onDisposition(alert, "escalated")}>Escalate</button></div>}<div className="disclaimer">Review priority indicates a workflow state only. It is not a diagnosis.</div></div>) : <div className="empty-state">No alerts linked to this case.</div>}
        </section>
        <section className="card"><div className="card-heading"><div><h2>Evidence and source records</h2><p>All values below are synthetic demo records</p></div><span className="pill teal">{item.observations.length} records</span></div>
          <div className="table-wrap"><table><thead><tr><th>Observation</th><th>Value</th><th>Observed</th><th>Source / quality</th></tr></thead><tbody>{item.observations.map((observation) => <tr key={observation.id}><td><strong>{titleCase(observation.dataType)}</strong><br /><span className="muted small">{observation.id}</span></td><td>{observation.value} {observation.unit}</td><td>{formatTime(observation.observedAt)}</td><td>{observation.source}<br /><span className="muted">{titleCase(observation.quality)} · {observation.isSynthetic ? "Synthetic" : "Imported"}</span></td></tr>)}</tbody></table></div>
        </section>
      </div>
      <div>
        <section className="card"><div className="card-heading"><div><h2>Recommendation history</h2><p>Clinician-authored · timestamped</p></div></div>
          {item.recommendations.length ? item.recommendations.map((recommendation) => <div className="recommendation" key={recommendation.id}><span className={`pill ${recommendation.status === "acknowledged" ? "teal" : "blue"}`}>{titleCase(recommendation.status)}</span><p>{recommendation.content}</p><small>Author: {recommendation.authorName} · {formatTime(recommendation.createdAt)}</small>{recommendation.followUps.map((followup) => <div className="followup-note" key={followup.id}><strong>Astronaut follow-up</strong><p>{followup.content}</p><small>{formatTime(followup.createdAt)}</small></div>)}</div>) : <div className="empty-state">No clinician recommendation recorded.</div>}
        </section>
        <section className="card"><div className="card-heading"><div><h2>Clinician recommendation</h2><p>Author is taken from your signed-in account</p></div></div>
          <form className="form-grid" onSubmit={(event) => { event.preventDefault(); onRecommend(event.currentTarget); event.currentTarget.reset(); }}>
            <input type="hidden" name="case_id" value={item.id} />
            <div className="field"><label htmlFor="recommendation-type">Follow-up type</label><select id="recommendation-type" name="recommendation_type"><option value="information_request">Information request</option><option value="follow_up">Follow-up</option><option value="consultation">Consultation</option></select></div>
            <div className="field"><label htmlFor="recommendation-content">Recommendation / question</label><textarea id="recommendation-content" name="content" required minLength="10" maxLength="1200" placeholder="Write the follow-up for the astronaut. Avoid unapproved medical instructions." /></div>
            <div className="field"><label htmlFor="follow-up-due">Requested follow-up date (optional)</label><input id="follow-up-due" name="follow_up_due_at" type="datetime-local" /></div>
            <button className="btn primary" disabled={working} type="submit">Send clinician-authored follow-up</button>
          </form>
        </section>
      </div>
    </div>
  </>;
}

function CheckInView({ onSubmit, working }) {
  return <>
    <Heading kicker="Astronaut portal" title="Symptom check-in" description="Share a self-reported update with the assigned medical team." />
    <section className="card checkin-card"><div className="card-heading"><div><h2>How are you feeling?</h2><p>Your report will be added to a case for the assigned medical team.</p></div><span className="pill teal">Self-reported</span></div>
      <form className="form-grid" onSubmit={(event) => { event.preventDefault(); onSubmit(event.currentTarget); }}>
        <div className="field"><label>Symptoms <span className="muted">(select all that apply)</span></label><div className="check-options">{["Dizziness", "Fatigue", "Headache", "Nausea", "Sleep concern", "Other"].map((symptom) => <label key={symptom} className="check-option"><input type="checkbox" name="symptoms" value={symptom.toLowerCase().replaceAll(" ", "_")} /><span>{symptom}</span></label>)}</div></div>
        <div className="field"><label htmlFor="severity">Self-reported severity</label><select id="severity" name="severity" required defaultValue=""><option value="" disabled>Choose 1–5</option><option value="1">1 · Mild</option><option value="2">2 · Noticeable</option><option value="3">3 · Moderate</option><option value="4">4 · Significant</option><option value="5">5 · Severe</option></select></div>
        <div className="field"><label htmlFor="symptom-trend">How has it changed?</label><select id="symptom-trend" name="trend" required defaultValue=""><option value="" disabled>Choose a trend</option><option value="improving">Improving</option><option value="unchanged">Unchanged</option><option value="worsening">Worsening</option><option value="unknown">Unsure</option></select></div>
        <div className="field"><label htmlFor="symptom-description">Anything else to share? <span className="muted">(optional)</span></label><textarea id="symptom-description" name="description" maxLength="1000" placeholder="Add context for the medical team." /></div>
        <div className="safety-note">Submission does not guarantee immediate review. This prototype is not an emergency service. Follow approved mission emergency procedures.</div>
        <button className="btn primary" type="submit" disabled={working}>{working ? "Submitting…" : "Submit check-in"}</button>
      </form>
    </section>
  </>;
}

function RecommendationsView({ cases, onAcknowledge, onFollowUp, working }) {
  const recommendations = cases.flatMap((item) => item.recommendations.map((recommendation) => ({ ...recommendation, caseTitle: item.title })));
  return <>
    <Heading kicker="Astronaut portal" title="Care follow-up" description="Review messages authored by the assigned clinician." />
    <div className="recommendations-list">{recommendations.length ? recommendations.map((recommendation) => <section className="card" key={recommendation.id}>
      <div className="card-heading"><div><h2>{recommendation.caseTitle}</h2><p>By {recommendation.authorName} · {formatTime(recommendation.createdAt)}</p></div><span className={`pill ${recommendation.status === "acknowledged" ? "teal" : "blue"}`}>{titleCase(recommendation.status)}</span></div>
      <p className="recommendation-content">{recommendation.content}</p>
      {recommendation.dueAt && <p className="muted small">Requested by {formatTime(recommendation.dueAt)}</p>}
      {recommendation.status === "sent" && <button disabled={working} className="btn primary" onClick={() => onAcknowledge(recommendation.id)}>Acknowledge receipt</button>}
      {recommendation.followUps.map((followup) => <div className="followup-note" key={followup.id}><strong>Your follow-up</strong><p>{followup.content}</p><small>{formatTime(followup.createdAt)}</small></div>)}
      {!recommendation.followUps.length && recommendation.status === "acknowledged" && <FollowUpForm disabled={working} onSubmit={(content) => onFollowUp(recommendation.id, content)} />}
    </section>) : <section className="card empty-state">No clinician-authored follow-up has been sent yet.</section>}</div>
  </>;
}

function FollowUpForm({ onSubmit, disabled }) {
  return <form className="follow-up-form" onSubmit={(event) => {
    event.preventDefault();
    const form = event.currentTarget;
    const content = new FormData(form).get("followup");
    onSubmit(content);
    form.reset();
  }}>
    <div className="field"><label>Submit requested follow-up</label><textarea name="followup" required minLength="2" maxLength="1000" placeholder="Share your response with the medical team." /></div>
    <button className="btn" disabled={disabled} type="submit">Send follow-up response</button>
  </form>;
}

function AdminView({ data, onReset }) {
  const summary = data?.summary || { accounts: 0, cases: 0, auditEvents: 0 };
  return <>
    <Heading kicker="System administration" title="Demo system overview" description="Synthetic environment status and technical activity.">
      <button className="btn danger" onClick={() => { if (window.confirm("Reset the synthetic demo cases, alerts and recommendations?")) onReset(); }}>Reset demo data</button>
    </Heading>
    <div className="admin-stat-row"><div className="admin-stat"><strong>{summary.accounts}</strong><small>Demo accounts</small></div><div className="admin-stat"><strong>{summary.cases}</strong><small>Synthetic cases</small></div><div className="admin-stat"><strong>{summary.auditEvents}</strong><small>Audit events</small></div></div>
    <section className="card"><div className="card-heading"><div><h2>Audit log</h2><p>Technical access and workflow events; no symptom descriptions</p></div><span className="pill blue">Technical metadata only</span></div>
      <div className="table-wrap"><table><thead><tr><th>Time</th><th>Actor</th><th>Role</th><th>Action</th><th>Object</th><th>Outcome</th></tr></thead><tbody>{(data?.audit || []).map((event) => <tr key={event.id}><td>{formatTime(event.occurredAt)}</td><td>{event.actorName}</td><td>{titleCase(event.role)}</td><td><strong>{titleCase(event.action)}</strong></td><td>{event.objectType} · {event.objectId.slice(0, 12)}</td><td><span className="pill teal">{event.outcome}</span></td></tr>)}</tbody></table></div>
    </section>
    <section className="card"><div className="card-heading"><div><h2>System boundary</h2><p>Local prototype scope</p></div></div><p className="muted small">No live spacecraft, agency, external health system or medical sensor connection. Demo identity is not production authentication. Only synthetic records belong in this environment.</p></section>
  </>;
}

createRoot(document.getElementById("root")).render(<App />);
