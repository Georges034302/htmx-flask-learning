# Lesson 09: Trigger requests automatically on page load

Included step: 19

Learning objective:
Master one focused concept from step 19 with precise, sequential execution.

Editor notes:
- Keep the exact sequence from source material.
- Validate behavior at each test checkpoint before continuing.

## Detailed walkthrough

## 19) Trigger requests automatically on page load

Now you will learn another very important HTMX capability: `hx-trigger="load"`.

This allows HTMX to automatically fetch content immediately after the page loads, without user interaction.

Common uses:
- Dashboards
- Monitoring systems
- Analytics pages
- Activity feeds
- Admin portals

Goal:
- When the page opens, HTMX automatically requests data
- Flask returns HTML
- Content appears dynamically

### 19.1 Create a new route

Add this route in `app.py`:

```python
@app.route("/latest")
def latest():

    latest_updates = [
        "Server running normally",
        "3 new employees added",
        "Backup completed successfully"
    ]

    return render_template(
        "partials/latest.html",
        updates=latest_updates
    )
```

### 19.2 Create partial template

Create file: `templates/partials/latest.html`

```html
<h3>Latest Updates</h3>

<ul>
{% for update in updates %}
    <li>{{ update }}</li>
{% endfor %}
</ul>
```

### 19.3 Add auto-loading section to index.html

Add this below the search section:

```html
<hr>

<h2>Automatic Content Loading</h2>

<div
    hx-get="/latest"
    hx-trigger="load"
    hx-target="this">

    Loading latest updates...

</div>
```

Important concepts:
- `hx-trigger="load"`: trigger request automatically when element loads
- `hx-target="this"`: replace the element itself with returned HTML

### 19.4 Test it

Refresh browser.

Expected behavior:
- Page loads
- "Loading latest updates..." appears briefly
- HTMX requests `/latest` automatically
- Flask returns HTML fragment
- Content replaces the loading div

No user interaction required.

Observe Network tab:
- Refresh with DevTools open
- You should see automatic `/latest` request

What you learned:
- Automatic HTMX requests
- Load triggers
- Self-replacing components
- Async page initialization
- Dashboard-style rendering

