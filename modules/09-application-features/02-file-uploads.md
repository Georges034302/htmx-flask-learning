# Lesson 02: File Uploads

## Concept
File Uploads.


## 1. File Uploads

### Goal
Allow users to upload files from the dashboard. The file is sent via an HTMX form, validated server-side (type + size), saved to disk, and the result is rendered inline — no page refresh.

---

### 1.1 Configure upload folder (app.py)

```python
import os

app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(__file__), "uploads")
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024  # 2 MB limit
```

`MAX_CONTENT_LENGTH` causes Flask to automatically reject oversized uploads with a 413 error.

---

### 1.2 Create uploads/ directory

```bash
mkdir uploads
```

Files will be saved here server-side.

---

### 1.3 Add upload helpers and route (routes/main_routes.py)

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

### 1.4 Create upload result partial (templates/partials/upload_result.html)

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

### 1.5 Add upload form to dashboard (templates/index.html)

```html
<h2>File Upload</h2>

<form
    hx-post="/upload-file"
    hx-target="#upload-result"
    hx-encoding="multipart/form-data">
    <input type="file" name="file" accept=".png,.jpg,.jpeg,.gif,.pdf,.txt,.csv">
    <button type="submit" class="btn btn-primary">Upload</button>
</form>

<div id="upload-result"></div>
```

`hx-encoding="multipart/form-data"` is required for file uploads with HTMX.

---

### 1.6 CSS — static/css/main.css

Upload result feedback uses `.flash.flash-success` / `.flash.flash-error` from `main.css`:

```html
<div class="flash flash-{{ status }}">{{ message }}</div>
```

No custom CSS is needed.

---

### 1.7 Test cases

| Action                          | Expected result                          |
|---------------------------------|------------------------------------------|
| Upload a `.txt` file            | Success: "Uploaded: filename.txt"        |
| Submit with no file selected    | Error: "No file selected."               |
| Upload a `.exe` file            | Error: "File type not allowed."          |
| Upload file > 2 MB              | Flask returns 413 Request Entity Too Large |

---

