# Lesson 07: Trigger requests automatically on page load

## Concept
Trigger requests automatically on page load.


## 1. Trigger requests automatically on page load

This allows HTMX to automatically fetch content immediately after the page loads, without user interaction.

Common uses:
- Dashboards
- Monitoring systems
- Analytics pages
- Activity feeds
- Admin portals

- When the page opens, HTMX automatically requests data
- Flask returns HTML
- Content appears dynamically

### 1.1 Create a new route

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

### 1.2 Create partial template

Create file: `templates/partials/latest.html`

```html
<h3>Latest Updates</h3>

<ul>
{% for update in updates %}
    <li>{{ update }}</li>
{% endfor %}
</ul>
```

### 1.3 Add auto-loading section to index.html

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

- `hx-trigger="load"`: trigger request automatically when element loads
- `hx-target="this"`: replace the element itself with returned HTML

### 1.4 Test it

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

