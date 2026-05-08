# Lesson 31: Add Polling with Automatic Table Refresh

Included step: 41

Learning objective:
Master one focused concept from step 41 with precise, sequential execution.

Editor notes:
- Keep the exact sequence from source material.
- Validate behavior at each test checkpoint before continuing.

## Detailed walkthrough

## 41) Add Polling with Automatic Table Refresh

### Goal
Keep the employee table synchronized by auto-refreshing at a fixed interval.

### 41.1 Updated employee table container (templates/index.html)

Changed trigger from:

```html
hx-trigger="load, employee-added from:body"
```

to:

```html
hx-trigger="load, every 5s, employee-added from:body"
```

### 41.2 Behavior

- Table loads on initial page render.
- Table refreshes every 5 seconds automatically.
- Table also refreshes immediately on `employee-added` event.

Current implementation note:
- The table container includes `hx-include="#employee-search"` so polling and event refreshes preserve the active search query. If the search input is cleared, the full table is shown again.

No manual action or page refresh is required.

### 41.3 Operational note

Polling improves synchronization but adds recurring server requests. Choose interval based on context (`5s`, `10s`, `30s`, etc.) to balance freshness and load.

### What you learned
- HTMX polling with `every 5s`
- Periodic trigger-based synchronization
- Live dashboard behavior without custom timer code
- Simple server-driven refresh architecture

---

