---
id: S9-lcrsq
status: closed
deps: []
links: []
created: 2026-08-01T22:49:45Z
type: task
priority: 2
assignee: Stavros Korokithakis
external-ref: STA-95
---
# Stars: extend catalogue to magnitude 6

The projection was zoomed ~2x to fill the frame, spreading the same 1637 stars over ~4x the area, so the sky looks sparse. User asked to go to a higher magnitude and regenerate.

Set MAGNITUDE_LIMIT in tools/make-stars.py to 6.0 (the naked-eye limit), regenerate tools/stars.js, and update the catalogue embedded in index.html. Expect roughly 5000 stars, about 3x the current count, taking stars.js from ~39KB to ~115KB and index.html from ~51KB to ~130KB. That is acceptable for a single static file.

Two things to check, not just mechanical regeneration:

1. The brightness and radius mappings in the star layer were tuned for a magnitude-5 cut: brightness = max(0.2, 1 - (magnitude + 1.5) / 8) and radius = 0.45 + (5.2 - magnitude) * 0.27. At magnitude 6 the radius falls to about 0.23px and brightness clamps at the 0.2 floor, so the new faint stars may be nearly invisible, which would defeat the point of adding them. Check a capture and adjust those constants if needed so the faint stars actually register as a dim dust of light without making the bright stars bloom.

2. Per-frame cost. The star layer does one arc plus fill per star per frame, so this triples that work. Measure before and after and report both.

Also update README.md, which says the tool emits stars brighter than magnitude 5.

Non-goals: no change to the projection, the aurora, or the meteors.

## Acceptance Criteria

Sky density looks close to what it was before the zoom. Faint stars are visible as dim specks, bright stars unchanged. Per-frame cost reported and still reasonable.


## Notes

**2026-08-01T22:49:50Z**

ready for implementation (direct user request)
