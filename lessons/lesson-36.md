# Lesson 36: File Uploads

Included step: 46

Learning objective:
Master one focused concept from step 46 with precise, sequential execution.

Editor notes:
- Keep the exact sequence from source material.
- Validate behavior at each test checkpoint before continuing.

## Detailed walkthrough

## 46) File Uploads

### Goal
Allow users to upload files from the dashboard. The file is sent via an HTMX form, validated server-side (type + size), saved to disk, and the result is rendered inline — no page refresh.

---

### 46.1 Configure upload folder (app.py)

```python
import os

app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(__file__), "uploads")
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024  # 2 MB limit
```

`MAX_CONTENT_LENGTH` causes Flask to automatically reject oversized uploads with a 413 error.

---

### 46.2 Create uploads/ directory

```bash
mkdir uploads
```

Files will be saved here server-side.

---

### 46.3 Add upload helpers and route (routes/main_routes.py)

Imports added:

```python
import os
from werkzeug.utils import secure_filename
from flask import current_app

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "pdf", "txt", "csv"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
```

Route:

```python
@main.route("/upload-file", methods=["POST"])
@login_required
def upload_file():
    file = request.files.get("file")

    if not file or file.filename == "":
        return render_template("partials/upload_result.html", error="No file selected.")

    if not allowed_file(file.filename):
        return render_template("partials/upload_result.html",
            error=f"File type not allowed. Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}.")

    filename = secure_filename(file.filename)
    save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    file.save(save_path)

    return render_template("partials/upload_result.html", filename=filename)
```

`secure_filename` sanitizes the filename to prevent path traversal attacks.

---

### 46.4 Create upload result partial (templates/partials/upload_result.html)

```html
{% if error %}
<div class="upload-result error">{{ error }}</div>
{% elif filename %}
<div class="upload-result success">
    <strong>Uploaded:</strong> {{ filename }}
</div>
{% endif %}
```

---

### 46.5 Add upload form to dashboard (templates/index.html)

```html
<h2>File Upload</h2>

<form
    hx-post="/upload-file"
    hx-target="#upload-result"
    hx-encoding="multipart/form-data">
    <input type="file" name="file" accept=".png,.jpg,.jpeg,.gif,.pdf,.txt,.csv">
    <button type="submit">Upload</button>
</form>

<div id="upload-result"></div>
```

`hx-encoding="multipart/form-data"` is required for file uploads with HTMX.

---

### 46.6 Add upload CSS (static/style.css)

```css
.upload-result {
    padding: 10px 14px;
    margin-top: 10px;
    border-radius: 5px;
}

.upload-result.success { background-color: #d4edda; color: #155724; }
.upload-result.error   { background-color: #f8d7da; color: #721c24; }
```

---

### 46.7 Test cases

| Action                          | Expected result                          |
|---------------------------------|------------------------------------------|
| Upload a `.txt` file            | Success: "Uploaded: filename.txt"        |
| Submit with no file selected    | Error: "No file selected."               |
| Upload a `.exe` file            | Error: "File type not allowed."          |
| Upload file > 2 MB              | Flask returns 413 Request Entity Too Large |

---

### What you learned
- `hx-encoding="multipart/form-data"` for HTMX file uploads
- `secure_filename` for path traversal prevention
- Server-side file type whitelisting
- `MAX_CONTENT_LENGTH` for size enforcement
- `current_app` for accessing config inside Blueprints
- Inline upload feedback with HTMX partials

---

---

