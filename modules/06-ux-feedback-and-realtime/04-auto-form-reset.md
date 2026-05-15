# Lesson 04: Clear the Form Automatically After Successful Submission

## Concept
Clear the Form Automatically After Successful Submission.


## 1. Clear the Form Automatically After Successful Submission

### Goal
Clear the add-employee form automatically after a successful submission, so the UI is immediately ready for the next entry.

### 1.1 Confirmed form id in templates/index.html

The form already has:

```html
<form
    id="employee-form"
    hx-post="/add-employee"
    hx-target="#form-result">
```

### 1.2 Added event listener script in templates/index.html

Inserted before `</body>`:

```html
<script>
document.body.addEventListener("employee-added", function () {
    document.getElementById("employee-form").reset();
});
</script>
```

This listens for the `employee-added` custom event (already emitted by the backend) and calls `.reset()` on the form.

### 1.3 Behavior

After successful add:
- employee is saved
- flash message appears
- table refreshes
- form fields clear automatically

No page refresh is required.

**Note:** This is minimal JavaScript. The backend remains the source of truth by emitting events; the frontend only reacts to those events.

