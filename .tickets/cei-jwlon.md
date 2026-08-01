---
id: cei-jwlon
status: closed
deps: []
links: []
created: 2026-08-01T09:42:08Z
type: task
priority: 2
assignee: Stavros Korokithakis
---
# index.html skeleton: fullscreen black canvas

Objective: create index.html, a single self-contained static page (all CSS/JS inline, no dependencies, no network).
- Fullscreen canvas, pure black background, resizes with window.
- requestAnimationFrame render loop.
- Cursor auto-hides after ~2s of no mouse movement.
- Location config: const default lat=40.64, lon=22.94 (Thessaloniki), overridable via URL params ?lat=..&lon=..
- Structure the loop so later tasks can add layers (stars, aurora, meteors) cleanly.
Non-goals: no settings UI, no audio.

## Acceptance Criteria

Opening index.html shows a black fullscreen canvas; cursor disappears when idle; lat/lon params parsed.


## Notes

**2026-08-01T09:45:51Z**

ready for implementation
