---
id: cei-ponfw
status: closed
deps: [cei-iuxyn, cei-jwlon]
links: []
created: 2026-08-01T09:42:18Z
type: task
priority: 2
assignee: Stavros Korokithakis
---
# Live accurate star rendering

Objective: render the real night sky overhead, zenith-centered, in index.html.
- Embed the star data from tools/stars.js inline into index.html.
- Compute local sidereal time from current Date and longitude; transform each star RA/Dec -> alt/az for the configured lat/lon; drop stars below the horizon (keep alt > ~0).
- Project with a zenith-centered projection (stereographic or equidistant from zenith) filling the canvas; zenith at screen center.
- Star size and brightness follow magnitude (brighter = larger/brighter). Subtle per-star twinkle is welcome but keep it gentle.
- Recompute positions continuously or at least every few seconds so the sky rotates in real time.
- Sanity check: for Thessaloniki the sky should match reality (e.g. compare a few bright stars against a planetarium site for the current time).
Non-goals: no constellation lines/labels, no planets/moon, no atmospheric refraction.

## Design

Standard formulas: GMST from Julian date, LST = GMST + lon, hour angle H = LST - RA, then alt/az from lat/dec/H. ~100 lines, no libraries.

## Acceptance Criteria

Stars visible and correctly placed for current time in Thessaloniki; bright stars clearly brighter; sky orientation sensible (north up or documented).


## Notes

**2026-08-01T09:45:51Z**

ready for implementation

**2026-08-01T10:08:21Z**

Done. Review checkpoint: fixed east/west mirror for ceiling (upward) view. Skipped precession (~0.3deg, invisible) and binary-star dedup (combined light is physically right).
