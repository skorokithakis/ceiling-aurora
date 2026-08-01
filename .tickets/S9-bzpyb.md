---
id: S9-bzpyb
status: closed
deps: []
links: []
created: 2026-08-01T16:51:30Z
type: task
priority: 2
assignee: Stavros Korokithakis
external-ref: STA-95
---
# Aurora: more connective haze, faster motion

User feedback on the shipped curtain aurora (commit 0660cf8): 'much better, but the auroras aren't connected enough. There should be more wispy connections between them, and the motion should be faster.'

Two changes to the aurora layer in index.html. Nothing else.

1. More wispy connective structure between the filaments. The rays currently read as somewhat separate columns. They need more visible material joining them so they belong to one sheet. Note this is not simply 'raise the body pass alpha' — flat haze was rejected earlier in tuning for looking like fog. It wants wispy, uneven, structured connective material: horizontal or diagonal streaks and varying-density bridges between neighbouring rays, not a uniform wash.
2. Faster motion overall. Roughly double the current rate as a starting point. Keep it smooth; no jitter or strobing.

Non-goals: do not retune brightness, saturation, filament width or spacing. Do not change the star or meteor layers. Do not touch the two-pass structure or the uniform-t sampling.

Caveat: the look took eight rounds to settle and is easy to regress. Read the comment at the top of the aurora layer listing the things that made it look fake, and check captures against that list before reporting.

## Acceptance Criteria

Filaments read as one connected curtain rather than separate columns, with uneven wispy joining material rather than flat haze. Motion is clearly quicker while staying calm. Per-frame cost stays under 16ms.


## Notes

**2026-08-01T16:51:36Z**

ready for implementation (direct user request)

**2026-08-01T17:04:22Z**

Round 1 captures are invalid — they do not show the code in the working tree.

All five aurora-r10 PNGs show three thick, blurred, wavy horizontal ribbons in green and magenta. That is the PRE-STA-95 aurora, the one with hues 128/142/320 from commit 2ea8412. That code no longer exists in index.html. The curtain renderer is not in these images at all.

So the capture pipeline is loading a stale copy of the page. Most likely the browser HTTP/disk cache, or a copy of index.html left in a temp directory. The 31-line diff itself looks reasonable and cannot possibly produce that output.

Fix the capture before judging anything: disable the cache in the CDP session (Network.setCacheDisabled) or append a cache-busting query string, and add a positive check that the render matches the working tree before reporting — the earlier rounds silently passed because the file happened to be fresh.

This also means the two-second pairs prove nothing about the new speed, and the 5.87ms per frame figure was measured against the old renderer. Re-do all of it.

**2026-08-01T19:46:48Z**

Additional user feedback: 'it skews left too much, the right side is empty of stars and auroras'.

Aurora part — real and fixable. The curtain offsets and spans favour the left. In aurora-r8-1920x1080 and aurora-r9-1920x1080 the sash runs from roughly x=150 to x=1500 on a 1920 frame, leaving about 400px of dead space on the right and almost none on the left. Centre the curtain placement and spread it wider so the sash is balanced across the frame.

Star part — NOT an aurora bug, and not asymmetric. Line 1725-1727: centerX = width/2, centerY = height/2, horizonRadius = min(width, height)/2. The star field is therefore a circle centred in the frame with radius = height/2 on a 16:9 display, so about 240px on EACH side has no stars by construction. It is symmetric; any left-heaviness the user sees is either the aurora bias above or genuine sparsity in the real sky at that moment. Whether to fill the frame instead is a separate decision — asked the user.
