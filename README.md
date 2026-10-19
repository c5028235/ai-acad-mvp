# AI Explorers Academy — Mission 1 MVP

Runnable prototype: Django REST Framework backend and React/Vite frontend. A parent registers, adds a child aged 8–14, and children aged 8–10 can complete Mission 1, take a server-scored quiz, earn a badge and view parent-visible progress.

## Requirements
- Python 3.11+
- Node.js 20.19+ or 22+
- Optional: PostgreSQL 15+

## Backend setup
Open a terminal:

```bash
cd backend
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Windows PowerShell: Copy-Item .env.example .env
python manage.py makemigrations academy
python manage.py migrate
python manage.py seed_mission
python manage.py runserver
```

Leave the Django server running at `http://127.0.0.1:8000/`.

## Frontend setup
In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173/`. Register a parent account (use a strong password), add a nickname and age 8–10, then open Mission 1.

## Run tests

```bash
cd backend
python manage.py test academy
```

## API endpoints

| Method | Path | Function |
|---|---|---|
| POST | `/api/auth/register/` | Register parent |
| POST | `/api/auth/login/` | Get JWT tokens |
| POST | `/api/auth/refresh/` | Refresh access token |
| GET/POST | `/api/children/` | List/create parent-owned profiles |
| GET | `/api/missions/meet-ai/` | Mission activities and quiz questions (no answer keys) |
| GET | `/api/children/{id}/progress/` | Parent-only progress and badges |
| POST | `/api/children/{id}/missions/meet-ai/submit/` | Validate and score answers server-side |

Quiz request format: `{"answers":{"QUESTION_ID":1,"OTHER_QUESTION_ID":0,...}}`, with a response for each question. Correct answer indices are not exposed until after submission.

## Directory structure

```
backend/
  config/                 Django settings and routes
  academy/
    management/commands/seed_mission.py
    models.py             Curriculum, profiles, progress, attempts
    serializers.py        API response schemas
    views.py              Parent-scoped endpoints and scoring
    urls.py               API routes
    tests.py              Basic authorization and scoring tests
  manage.py
  requirements.txt
frontend/
  src/App.jsx             Parent dashboard and Mission 1 flow
  src/style.css           Responsive styles
  src/main.jsx
  package.json
```

## Data and child safety notes

This is a **local pilot MVP, not a production-ready child-facing service**. It does not include verified parental consent, robust account recovery, email verification, production logging/monitoring, content moderation, retention/deletion workflows, rate limiting, or a completed DPIA. Obtain appropriate parental consent and perform a UK GDPR / ICO Children's Code review before testing with real children or deploying publicly. The child's nickname and age are stored; the reflection textarea is intentionally not persisted. No generative AI API is used.

For production, set a strong `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=false`, configure HTTPS and secure cookie/header settings, production-grade deployment, database backups, refresh-token strategy and throttling. JWTs are kept **in React memory only** in this prototype; page refresh signs the parent out, intentionally avoiding localStorage token persistence.

The interactive lesson choices are client-rendered practice, while the final quiz is scored on the server. The backend validates parent ownership and target age. Passing the quiz awards 100 XP once; retries do not stack XP.

## Next milestones
1. Improve learning measurement with a pre-lesson baseline and independent post-lesson assessment.
2. Add parent consent and privacy/retention controls before child pilots.
3. Add Mission 2 and curriculum authoring workflow.
4. Add proper account recovery and deployment safeguards.
