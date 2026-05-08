# HTMX + Flask Learning Repository

This repository is a step-by-step learning project for building a modern, server-rendered web app with Flask and HTMX.

It is designed as a progressive curriculum, starting from environment setup and first requests, then moving through CRUD, reactive UI updates, UX patterns, authentication, uploads, and production/deployment concepts.

## Repository Purpose

- Teach practical HTMX + Flask patterns by building one coherent application.
- Keep frontend logic lightweight by shifting behavior to server-rendered partials.
- Provide reusable lessons that can stand alone as a learning track.

## What Is Implemented Today

Core app features currently available in this repository:

- Flask app with Blueprint-based route organization
- HTMX-driven dynamic UI interactions
- Employee CRUD with inline edit and row-level updates
- Search, sorting, pagination, and periodic polling
- Flash messages with category styling and auto-dismiss
- Session-based login/logout protection
- File upload endpoint with type checks and max-size limit
- Modal details view for employee records

## Lessons-First Structure

The complete learning path lives in the lessons folder.

- Start here: [lessons/index.md](lessons/index.md)
- Total lessons: 41
- Core implementation path: lessons 01-32, 35-36
- Advanced instructions-only path: lessons 33-34, 37-41

If you follow the lessons in order, you can build the full local website and then continue to production/deployment workflows.

## Quick Start

### 1) Create and activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Run the app

```bash
python app.py
```

Open http://127.0.0.1:5000 in your browser.

## Demo Credentials

Current mock login account:

- Username: `admin`
- Password: `password123`

Stored in [data/mock.py](data/mock.py).

## Tech Stack

- Python 3
- Flask
- HTMX
- Jinja2 templates
- Gunicorn (included dependency for production lessons)

## Repository Layout

- [app.py](app.py): Flask app entrypoint and config
- [routes/main_routes.py](routes/main_routes.py): application routes
- [templates/index.html](templates/index.html): main UI shell
- [templates/partials](templates/partials): server-rendered HTML fragments
- [static/style.css](static/style.css): app styling
- [data/mock.py](data/mock.py): in-memory mock dataset
- [lessons](lessons): curriculum content

## Notes

- This project intentionally demonstrates server-driven UI architecture.
- Some advanced lessons are marked instructions-only because they depend on external infrastructure (for example cloud subscriptions, CI secrets, or container runtime).

---
## Copyright and License

Copyright (c) 2026 Dr. Georges Bou Ghantous. All rights reserved.

License details are provided in [docs/license.md](docs/license.md).

<p><sub><em><span style="color:#808080;">🧑‍🏫 Dr. Georges Bou Ghantous</span></em></sub></p>

