---
id: S9-faaft
status: closed
deps: []
links: []
created: 2026-08-01T22:42:52Z
type: task
priority: 2
assignee: Stavros Korokithakis
external-ref: STA-95
---
# Star field: fill the frame instead of a centred circle

User: 'fill the frame please, it should be a bit more zoomed in. The ceiling isn't a 180 degree view.'

index.html line 1727: horizonRadius = Math.min(frame.width, frame.height) / 2. The zenith-centred projection therefore draws the whole hemisphere as a circle inscribed in the shorter side, leaving bare margins left and right on a 16:9 display.

Change horizonRadius so the projection covers the WHOLE frame including the corners — half the diagonal, not half the shorter side. On 1920x1080 that takes the radius from 540 to about 1101, roughly 2x zoom. The frame edge then sits around 78 degrees from zenith at the sides and the corners land on the horizon; sky below roughly 41 degrees elevation north and south is cropped, which is what the user wants.

Scope: horizonRadius only. Do not change centerX/centerY, the azimuth or altitude maths, the mirroring, star brightness or sizes. Do not touch the aurora or meteor layers.

Also update README.md: it currently only documents orientation. Add a sentence that the view is zoomed so it fills the frame, and that the lowest sky near the horizon is therefore cropped.

## Acceptance Criteria

Stars reach the frame edges and corners with no bare margins. Star positions are still correct relative to each other, just scaled. Nothing else changed.


## Notes

**2026-08-01T22:42:52Z**

ready for implementation (direct user request)

**2026-08-01T22:42:57Z**

ready for implementation (direct user request)
