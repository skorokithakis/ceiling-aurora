---
id: S9-ghily
status: closed
deps: [cei-coyjb]
links: []
created: 2026-08-01T14:57:22Z
type: task
priority: 2
assignee: Stavros Korokithakis
---
# Meteors: fade while still moving

Objective: make meteors keep travelling while they fade, instead of freezing at the end of their path and dimming in place.

Current behaviour in index.html (meteor layer, ~line 1822-1900): the head interpolates start->end over 'duration', the trail is drawn from the fixed birth point to the head, then for 'tailDuration' the whole full-length streak sits still and fades. Replace that two-phase model.

New model:
- One continuous flight. The head moves at constant velocity for the entire visible life (~0.7-1.1s). No frozen phase.
- The trail is a fixed-length segment BEHIND the head (~15-25% of the screen's short side). It grows from zero at spawn until it reaches full length, then follows the head.
- One brightness envelope over the life: fast rise (first ~15%), then decay to zero by the end. The meteor goes dark while it is still moving.
- Speed stays close to the current value, so the path becomes roughly 2-3x longer than now.
- Drop the 'keep both ends on screen' clamp. Spawn on screen, random direction; the meteor may exit through an edge.

Keep unchanged: spawn interval (60-180s), colours, line width, glow, layer order, head dot.

Caveat: createLinearGradient with two identical points is degenerate. Guard the spawn instant when tail and head coincide.

Non-goals: no terminal flare/burst, no meteor showers or radiant, no new config or UI, no changes to other layers.

## Acceptance Criteria

A meteor visibly continues to move while it fades out; it never stops and dims in place. The trail follows the head at a fixed length instead of stretching back to the birth point. Meteors stay rare and soft enough to keep the calm mood.


## Notes

**2026-08-01T14:57:37Z**

ready for implementation
