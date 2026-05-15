# Lesson 05: Add smart request timing with delay

## Concept
Add smart request timing with delay.

## 1. Add smart request timing with delay

Right now, every keystroke sends a request immediately.

This can generate unnecessary requests and server load.
Use `delay` to wait briefly and send only after typing pauses.

### 1.1 Update hx-trigger with debounce

Replace:

```html
hx-trigger="keyup"
```

WITH:

```html
hx-trigger="keyup changed delay:500ms"
```

Your FULL input should now become:

```html
<input
    type="text"
    name="query"
    placeholder="Type something..."
    hx-get="/search"
    hx-trigger="keyup changed delay:500ms"
    hx-target="#search-results">
```

- `keyup`: Trigger after keyboard interaction
- `changed`: Only send request if value actually changed
- `delay:500ms`: Wait 500 milliseconds before sending
- If user keeps typing: timer resets and request waits
- This is called **debouncing**
- In traditional JavaScript frameworks, this requires event listeners, timers, and state logic
- HTMX does it declaratively in HTML

### 1.2 Test it

Refresh your browser.

Now type quickly.

Observe:
- Requests do NOT fire instantly
- HTMX waits briefly
- Request happens after typing pauses

### 1.3 Inspect Network tab

Open DevTools → **Network**.

Type quickly.

You should now see:
- Fewer requests
- Cleaner request timing
- More efficient behavior

- This is debouncing expressed declaratively in HTML.

