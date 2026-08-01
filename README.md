# ceiling-aurora

A calm night-sky visualization to project onto your ceiling: the real stars
overhead right now, a slow aurora, and the occasional meteor. Pure black
background, single static HTML file, no dependencies.

## Use

Open <https://skorokithakis.github.io/ceiling-aurora/> (or `index.html`
locally), press F11, point the projector at the ceiling.

Default location is Thessaloniki. Override with URL parameters:

```
?lat=51.51&lon=-0.13
```

Orientation: north is at the top of the image, east on the left (the sky as
seen looking up). The view is zoomed to fill the frame, so the lowest sky
near the horizon is cropped.

## Regenerating star data

`tools/make-stars.py` downloads the HYG catalog and emits `tools/stars.js`
(stars brighter than magnitude 5). The data is embedded in `index.html`;
you only need this if you want to change the catalog.
