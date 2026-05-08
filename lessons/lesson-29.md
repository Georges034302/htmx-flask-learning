# Lesson 29: Clear the Form Automatically After Successful Submission

Included step: 39

Learning objective:
Master one focused concept from step 39 with precise, sequential execution.

Editor notes:
- Keep the exact sequence from source material.
- Validate behavior at each test checkpoint before continuing.

## Detailed walkthrough

## 39) Clear the Form Automatically After Successful Submission

### Goal
Clear the add-employee form automatically after a successful submission, so the UI is immediately ready for the next entry.

### 39.1 Confirmed form id in templates/index.html

The form already has:

```html
<form
    id="employee-form"
    hx-post="/add-employee"
    hx-target="#form-result">
```

### 39.2 Added event listener script in templates/index.html

Inserted before `</body>`:

```html
<script>
document.body.addEventListener("employee-added", function () {
    document.getElementById("employee-form").reset();
});
</script>
```

This listens for the `employee-added` custom event (already emitted by the backend) and calls `.reset()` on the form.

### 39.3 Behavior

After successful add:
- employee is saved
- flash message appears
- table refreshes
- form fields clear automatically

No page refresh is required.

### Architectural note
This is minimal, intentional JavaScript. The backend remains the source of truth by emitting events; the frontend only reacts to those events.

### What you learned
- HTMX custom event handling in plain JavaScript
- Form reset automation with `.reset()`
- Backend-triggered client behavior
- Minimal-JS enhancement pattern in HTMX apps
- Event-driven UX flow

---

