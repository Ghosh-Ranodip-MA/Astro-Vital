# ASTROVITAL X — React + FastAPI hackathon MVP

ASTROVITAL X is a synthetic-data prototype for the astronaut-to-clinician workflow. The app combines a React portal, a FastAPI API, SQLAlchemy persistence, a deterministic source-linked analysis rule, clinician-authored follow-up and astronaut acknowledgement/response.

**2026 NASA Space Apps challenge:** [Create Health Monitoring Software for Astronauts on Space Missions](https://www.spaceappschallenge.org/2026/challenges/health-monitoring-software/). The prototype addresses the challenge through a crew-facing health snapshot and self-report flow, source-linked trend review, and a human-led clinician follow-up loop. It does not use or claim access to NASA operational health data; all health observations are synthetic.

> **Scope and safety:** This is a local hackathon demo, not a medical device or emergency service. All health values and accounts are synthetic. The demo rule is not a medical threshold, diagnosis, or validated prediction. It does not measure vital signs or connect to a spacecraft, NASA, or external medical systems. Never enter real health information.

## Architecture

For the NASA Space Apps reviewer assessment, criterion-by-criterion findings, and a short presentation script, see [the project review](docs/ASTROVITAL_X/SPACE_APPS_REVIEW.md).

```text
React astronaut / doctor dashboards
              │ /api
              ▼
         FastAPI backend
          ┌───┴────┐
          ▼        ▼
 SQLAlchemy DB   Demo analysis engine
 SQLite local    deterministic rule
 PostgreSQL demo source-linked findings
          └───┬────┘
              ▼
         Case workflow
              ▼
 Recommendations → acknowledgement → follow-up response
```

The local Python default is SQLite so the MVP can run without a database service. Docker Compose runs the same API against PostgreSQL 16, alongside the React/Vite dev server.

## Quick start (local SQLite)

Requirements: Python 3.11+ and Node.js 18+.

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
npm install
```

In terminal 1:

```sh
uvicorn backend.main:app --reload --port 8000
```

In terminal 2:

```sh
npm run dev
```

Open [http://localhost:5173](http://localhost:5173). The API health check and interactive API docs are at `/api/health` and `http://localhost:8000/docs`.

## PostgreSQL run

With Docker Compose available:

```sh
docker compose up --build
```

Open [http://localhost:5173](http://localhost:5173). Compose starts PostgreSQL, waits for its health check, starts the FastAPI API, then serves the React client. The demo DB credentials in Compose are local-only and must not be used for deployment.

## Demo

1. Sign in as **Alex Demo** and inspect the synthetic readings/history; submit a symptom check-in.
2. Toggle **Offline**, submit a check-in and see its “queued locally — not delivered” state. Reconnect to sync with an idempotency key.
3. Sign in as **Dr. Maya Chen**, open the case and inspect the linked observations and deterministic trend flag.
4. Run the demo analysis, acknowledge/dismiss/escalate the flag, then author a follow-up recommendation.
5. Sign in as **Alex Demo** to acknowledge the recommendation and submit a follow-up response.
6. Sign in as **Mission Admin** to inspect technical audit events or reset the synthetic dataset.

The passwordless role selector is a local demonstration identity mechanism, not production authentication. It is not safe for deployment or exposure to a public network.

## Features

- React astronaut dashboard with profile, time-series chart, source/unit/time/quality metadata, and symptom check-in.
- FastAPI endpoints with role checks and explicit astronaut-to-clinician assignment enforcement.
- PostgreSQL-compatible normalized SQLAlchemy model for users, profile, observations, check-ins, cases, alerts, recommendations, follow-up responses and audit events.
- Deterministic `demo-trend-v1` trend review limited to valid, synthetic heart-rate records in `beats/min`, with source observation IDs, rule version and non-diagnostic caveats. This is not AI or a clinical threshold.
- Alert evidence links jump to and highlight the corresponding source observations in the case record.
- Clinician case queue, alert disposition (reason required to dismiss/escalate), authored recommendation, and follow-up lifecycle.
- Astronaut acknowledgement and follow-up response.
- Local offline queue with explicit un-delivered state and duplicate-safe synchronization.
- Admin technical audit view and dataset reset.

## Verify

```sh
pytest
npm run build
```

## Prototype limitations

- SQLite is the local default; PostgreSQL is configured in Docker Compose.
- Passwordless demo sessions are process-memory sessions; a server restart signs users out.
- Offline entries use browser local storage. This is not an encrypted/approved clinical offline store.
- The database schema is created at app startup for this MVP; production use needs migrations, managed authentication, hardened secrets/TLS, security review, privacy controls, and clinical governance.
- Analysis is a transparent deterministic demo rule, not a medical AI model. No diagnostic or predictive performance is claimed.
