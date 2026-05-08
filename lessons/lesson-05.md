# Lesson 05: Add smart request timing with delay

Included step: 15

Learning objective:
Master one focused concept from step 15 with precise, sequential execution.

Editor notes:
- Keep the exact sequence from source material.
- Validate behavior at each test checkpoint before continuing.

## Detailed walkthrough

## 15) Add smart request timing with delay

Right now, every keystroke sends a request immediately.

That works, but in real applications it can generate:
- Too many requests
- Unnecessary server load
- Poor UX

HTMX provides an elegant solution: **delay**

Goal:
- Instead of: Request on EVERY key
- We will make HTMX: Wait briefly while the user types, then only send after typing pauses
- This mimics professional live-search systems

### 15.1 Update hx-trigger with debounce

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

What this means:
- `keyup`: Trigger after keyboard interaction
- `changed`: Only send request if value actually changed
- `delay:500ms`: Wait 500 milliseconds before sending
- If user keeps typing: timer resets and request waits

Important concept:
- This is called **debouncing**
- In traditional JavaScript frameworks, this requires event listeners, timers, and state logic
- HTMX does it declaratively in HTML

### 15.2 Test it

Refresh your browser.

Now type quickly.

Observe:
- Requests do NOT fire instantly
- HTMX waits briefly
- Request happens after typing pauses

### 15.3 Inspect Network tab

Open DevTools → **Network**.

Type quickly.

You should now see:
- Fewer requests
- Cleaner request timing
- More efficient behavior

Important real-world relevance:
- This pattern is heavily used in search engines, filtering systems, dashboards, autocomplete systems, and admin panels

Mental shift:
- Instead of writing imperative JavaScript logic
- You describe behavior declaratively: `hx-trigger="keyup changed delay:500ms"`
- This is classic HTMX philosophy

What you just learned:
- HTMX event triggers
- Request timing
- Debounce behavior
- Reactive optimization
- Declarative frontend interaction

This is already professional-level frontend behavior.

