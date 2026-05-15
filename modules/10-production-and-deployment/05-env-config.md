# Lesson 05: Environment Configuration (.env and config classes)

## Concept
Environment Configuration (.env and config classes).


## 1. Environment Configuration (.env and config classes)

> **Instructions only** — no implementation required.

### Goal
Move hardcoded values (secret key, upload path, debug flag) out of source code into environment variables, with a Flask config class pattern for different environments (development, production).

---

### 1.1 Install python-dotenv

```bash
pip install python-dotenv
pip freeze > requirements.txt
```

---

### 1.2 Create .env file

Create `.env` in the project root:

```
FLASK_SECRET_KEY=change-me-in-production
FLASK_DEBUG=false
UPLOAD_FOLDER=uploads
MAX_UPLOAD_MB=2
```

Add `.env` to `.gitignore` — never commit secrets.

---

### 1.3 Create config.py

Create `config.py`:

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "fallback-dev-key")
    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", "uploads")
    MAX_CONTENT_LENGTH = int(os.environ.get("MAX_UPLOAD_MB", 2)) * 1024 * 1024

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
```

---

### 1.4 Update app.py

```python
from config import DevelopmentConfig, ProductionConfig
import os

app = Flask(__name__)

env = os.environ.get("FLASK_ENV", "development")
if env == "production":
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(DevelopmentConfig)
```

---

### 1.5 Add .env to .gitignore

```
.env
venv/
__pycache__/
uploads/
instance/
*.db
```

---

### 1.6 Environment variable flow

```
.env file (local dev)
  → python-dotenv loads into os.environ
  → config.py reads os.environ
  → app.py applies config class
  → routes use current_app.config["KEY"]

Production (Docker / Azure):
  → .env is not committed
  → environment variables set in container / Azure secrets
  → same config.py reads them transparently
```

---

