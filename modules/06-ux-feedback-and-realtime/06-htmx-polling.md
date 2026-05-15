# Lesson 06: Add Polling with Automatic Table Refresh

## Concept
Add Polling with Automatic Table Refresh.


## 1. Add Polling with Automatic Table Refresh

### Goal
Keep the employee table synchronized by auto-refreshing at a fixed interval.

### 1.1 Updated employee table container (templates/index.html)

Changed trigger from:

```html
hx-trigger="load, employee-added from:body"
```

to:

```html
hx-trigger="load, every 5s, employee-added from:body"
```

### 1.2 Behavior

- Table loads on initial page render.
- Table refreshes every 5 seconds automatically.
- Table also refreshes immediately on `employee-added` event.

Current implementation note:
- The table container includes `hx-include="#employee-search"` so polling and event refreshes preserve the active search query. If the search input is cleared, the full table is shown again.

> **`hx-include` explained:** Normally an HTMX request only sends values from within its own element. `hx-include` lets you include values from any other element (identified by CSS selector) in the request. Here it ensures the active search term is sent with every poll so the refreshed table stays filtered.

No manual action or page refresh is required.

### 1.3 Operational note

Polling improves synchronization but adds recurring server requests. Choose interval based on context (`5s`, `10s`, `30s`, etc.) to balance freshness and load.

