# Lesson 08: Replace vs append content with hx-swap

Included step: 18

Learning objective:
Master one focused concept from step 18 with precise, sequential execution.

Editor notes:
- Keep the exact sequence from source material.
- Validate behavior at each test checkpoint before continuing.

## Detailed walkthrough

## 18) Replace vs append content with hx-swap

Now you will learn how HTMX injects returned HTML into the page.

This is controlled by: `hx-swap`

Current behavior in this project:
- Input is configured with `hx-swap="beforeend"`
- Returned HTML is appended to existing content in `#search-results`

Default HTMX behavior (for reference):
- If `hx-swap` is omitted, HTMX uses `innerHTML`
- Existing content inside target gets replaced

Goal:
- Experiment with replacing content
- Experiment with appending content
- Understand DOM injection behavior

### 18.1 Add hx-swap (replace mode)

Update your input field with:

```html
hx-swap="innerHTML"
```

Full input:

```html
<input
    type="text"
    name="query"
    placeholder="Type something..."
    hx-get="/search"
    hx-trigger="keyup changed delay:500ms"
    hx-target="#search-results"
    hx-indicator="#loading"
    hx-swap="innerHTML">
```

What `innerHTML` means:
- Replace ONLY the inside of the target element
- The target container remains, its contents are replaced

### 18.2 Test current behavior

Refresh page and type: `a`

Results replace normally. This is expected.

### 18.3 Switch to beforeend (append mode)

Change:

```html
hx-swap="innerHTML"
```

To:

```html
hx-swap="beforeend"
```

What this means:
- Instead of replacing, HTMX appends returned HTML
- Conceptually similar to: `element.innerHTML += newContent`

Current implementation note:
- The live input in `templates/index.html` is now set to `hx-swap="beforeend"`.
- To go back to replacement behavior, change it to `hx-swap="innerHTML"`.

### 18.4 Test again

Refresh page, then type:
- `a`
- `b`
- `c`

Observe:
- Results keep appending

Important observation:
- You are now controlling DOM insertion strategy
- Content placement behavior
- UI rendering mechanics
- Directly from HTML attributes

