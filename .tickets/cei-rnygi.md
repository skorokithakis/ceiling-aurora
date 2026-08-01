---
id: cei-rnygi
status: closed
deps: [cei-jwlon]
links: []
created: 2026-08-01T09:42:25Z
type: task
priority: 2
assignee: Stavros Korokithakis
---
# Aurora layer

Objective: add a calm aurora effect over the starfield in index.html.
- 2-4 soft ribbons of light drifting slowly; colors drift through teal/green/violet.
- Very slow motion: visible change over seconds. No sharp edges; use gradients/blur or layered noise.
- Aurora renders above stars but must stay translucent enough that stars remain visible through it.
- Keep it cheap: should not tank framerate (offscreen canvas at reduced resolution scaled up is a fine trick).
Non-goals: no audio reactivity, no interaction.

## Acceptance Criteria

Aurora visibly flows on black background; stars still visible; animation smooth.


## Notes

**2026-08-01T09:45:51Z**

ready for implementation
