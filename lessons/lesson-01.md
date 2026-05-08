# Lesson 01: Environment and Flask Foundations

Included steps: 1-6

Learning objective:
Build a clean Python and Flask baseline so all later HTMX work runs consistently.

Editor notes:
- This lesson intentionally groups setup actions to reduce context switching.
- Keep command order exactly as written for reproducibility.

## Included steps
- Step 1) Check Python version
- Step 2) Create virtual environment
- Step 3) Activate virtual environment
- Step 4) Add ignore rules
- Step 5) Install Flask
- Step 6) Create and verify requirements file

## Detailed walkthrough

## 1) Check Python version

```bash
python --version || python3 --version
```

Observed version:
- Python 3.12.1


## 2) Create virtual environment

```bash
python3 -m venv venv
```

Verified with:

```bash
ls -ld venv
```


## 3) Activate virtual environment

```bash
source venv/bin/activate
```

Verified with:

```bash
echo "$VIRTUAL_ENV"
which python
python --version
```

Expected verification:
- VIRTUAL_ENV points to `<repo>/venv`
- Python path points to `<repo>/venv/bin/python`
- Python version is 3.12.1


## 4) Add ignore rules

Created `.gitignore` with:

```gitignore
venv/
.vscode/
```


## 5) Install Flask

```bash
source venv/bin/activate && pip install flask
```

Verified with:

```bash
pip show flask
```

Installed version:
- Flask 3.1.3

Package listing:

```bash
source venv/bin/activate && pip list
```

Installed packages at that time:
- blinker 1.9.0
- click 8.3.3
- Flask 3.1.3
- itsdangerous 2.2.0
- Jinja2 3.1.6
- MarkupSafe 3.0.3
- pip 23.2.1
- Werkzeug 3.1.8


## 6) Create and verify requirements file

```bash
source venv/bin/activate
pip freeze > requirements.txt
cat requirements.txt
pip install -r requirements.txt
pip freeze > requirements.txt
```

Notes:
- `cat requirements` was intended, but the actual file is `requirements.txt`.
- Reinstalling from `requirements.txt` confirmed all packages were already satisfied.

