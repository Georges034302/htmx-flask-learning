# Lesson 30: Add Auto-Dismissing Flash Messages

Included step: 40

## Concept
Add Auto-Dismissing Flash Messages.


## 40) Add Auto-Dismissing Flash Messages

### Goal
Make flash messages disappear automatically after a short delay to reduce UI clutter.

### 40.1 Updated messages partial (templates/partials/messages.html)

Message container class updated from:

```html
<div class="message">
```

to:

```html
<div class="message auto-dismiss">
```

`auto-dismiss` is used by JavaScript to target removable notifications.

### 40.2 Updated script in templates/index.html

Added an HTMX lifecycle listener:

```html
document.body.addEventListener("htmx:afterSwap", function () {
    const messages = document.querySelectorAll(".auto-dismiss");
    messages.forEach(function (message) {
        setTimeout(function () {
            message.remove();
        }, 3000);
    });
});
```

How it works:
- HTMX swaps new message HTML into the page.
- `htmx:afterSwap` fires.
- Each `.auto-dismiss` message is removed after 3 seconds.

### 40.3 Test

Add an employee:
- message appears
- stays visible briefly
- disappears automatically (~3 seconds)

No page refresh required.

