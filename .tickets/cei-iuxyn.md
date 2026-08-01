---
id: cei-iuxyn
status: closed
deps: []
links: []
created: 2026-08-01T09:42:05Z
type: task
priority: 2
assignee: Stavros Korokithakis
---
# Star catalog data pipeline

Objective: produce the embedded star data for the ceiling visualization.
- Write tools/make-stars.py: downloads the HYG star database (https://github.com/astronexus/HYG-Database, CSV), filters to magnitude <= 5.0, outputs a compact JS array of [ra_hours, dec_degrees, magnitude] rounded to sensible precision (~2-3 decimals).
- Output should be a single JS const declaration written to stdout or a file, ready to paste/embed into index.html.
- Run it once and commit the generated data as tools/stars.js (index.html embedding happens in a later task).
Non-goals: no star names, no constellation data, no proper motion.
Constraints: script is throwaway-quality but kept in repo for reproducibility. Target data size roughly 30-60 KB.

## Acceptance Criteria

tools/make-stars.py exists and runs; tools/stars.js contains ~1500-2000 stars as [ra,dec,mag] triples; brightest stars (Sirius mag -1.46, Vega, Arcturus) present.


## Notes

**2026-08-01T09:45:51Z**

ready for implementation
