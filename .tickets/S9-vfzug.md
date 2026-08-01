---
id: S9-vfzug
status: closed
deps: []
links: []
created: 2026-08-01T15:13:57Z
type: task
priority: 2
assignee: Stavros Korokithakis
external-ref: STA-95
---
# Aurora: render as vertical curtains instead of wavy bands

Objective: the aurora in index.html currently reads as fake. It is three thick, blurred, wavy horizontal strokes. Replace it with a curtain renderer so it looks like a real aurora: a vertical sash of light made of many thin rays.

Scope: only the aurora layer in index.html (the layers.push block that uses auroraCanvas, around line 1765). Do not touch the star layer or the meteor layer.

What must change:
1. Vertical rays. Sample points along each curtain's base path and draw a vertical line at each one, instead of stroking one thick horizontal path. Rays point to the top of the image (screen-space vertical).
2. Asymmetric edge. Bright and reasonably defined at the base of the curtain, fading to fully transparent at the top. Not a symmetric soft blob.
3. Folds. Slow, low-frequency variation of ray brightness and height along the curtain, so parts of it look like they turn toward the viewer. This is what gives the 3D look.
4. Filaments. Higher-frequency variation on top of the folds, so thin bright rays appear and dissolve within the sash.
5. Additive light: use globalCompositeOperation = 'lighter' on the offscreen canvas so overlapping sheets add up instead of going muddy.

Non-goals:
- No radial/corona aurora. The rays are screen-space vertical, even though the star field is a zenith projection. This was decided with the user.
- No WebGL, no shaders, no libraries. Keep it 2D canvas in the single static HTML file.
- No settings, no interaction, no new URL parameters.
- Do not change the meteor or star code.

Constraints:
- Must stay calm and slow. Visible change over seconds, no flicker, no strobing. This is projected on a ceiling for sleep.
- Stars must still be visible through the aurora. Keep it translucent.
- Keep it cheap. The layer renders to an offscreen canvas at reduced resolution and is scaled up; keep that trick.

Verification: google-chrome is installed. Run it headless to screenshot index.html at a few different times and confirm the look. Report the screenshot paths back so they can be reviewed.

## Design

Caveats found while planning:

- The current blur(5px) at auroraScale 4 will destroy the vertical rays. Reduce the blur, and lower auroraScale (2 or 3) if needed so filaments survive. Trade this against framerate; measure, do not guess.
- Colour: the body is green (hue ~125-140). Keep pink/magenta (~320) as a faint fringe near the TOP of the curtain only, at low alpha. Do not tint the whole sash pink.
- Cheap pseudo-noise is fine and preferred over a real noise implementation: a product or sum of a few sine terms at different spatial frequencies with slowly drifting phases gives both the folds and the filaments.
- 2-3 curtains is enough. More will just wash the sky out and hide the stars.
- Because rays are drawn per sample point, the x step controls both cost and filament thickness. This is the main tuning knob.

## Acceptance Criteria

A headless screenshot shows a curtain of light with visible vertical striations, brighter at its base and fading out at the top, with uneven brightness along its length. Stars remain visible. Motion stays slow and calm.


## Notes

**2026-08-01T15:17:30Z**

ready for implementation

**2026-08-01T15:27:40Z**

Round 1 rejected by architect. Reads as green fog over a dark wavy silhouette, not an aurora.

Findings from the screenshots:
1. The curtain is far too big. It spans the full width and most of the height, so three additive curtains sum into a haze. The sky should stay mostly black with a defined sash in it.
2. The lower border is a long, smooth, near-horizontal dark cut. It reads as a mountain ridge, not as light. A real aurora lower border is bright and crisp; here the eye sees the black below it instead.
3. The striations are invisible. They read as faint moire, not as rays. Real rays are thin, high contrast, with bright cores.
4. No folds. The sash is flat. This was the main 3D cue in the brief and it is missing.
5. Almost no visible change between t=10s and t=30s.

Direction for round 2 (this replaces the 'base path plus vertical rays' sampling scheme):

Model the curtain foot as a parametric curve sampled at UNIFORM t, not uniform x. Let x(t) wobble, e.g. x(t) = t*width + A*sin(w*t + phase). Draw one ray at each sample. Where dx/dt is small the rays bunch up and the light adds, so folds, curls and bright knots appear on their own from the geometry. This is also what really happens: a fold is the curtain seen edge-on. Do not fake folds with a brightness multiplier.

Also:
- 2 curtains, not 3. Each covers only part of the width and fades out at both ends. Leave black sky around and above the sash.
- Rays must be thin and high contrast. Vary per-ray brightness and height strongly, so bright filaments stand out against dim neighbours.
- Do not let the lower border be a smooth horizontal line across the whole frame. Give it slope and let it leave the frame, or add a soft glow below it so it does not cut to black.
- Raise saturation and the peak brightness of the ray cores. The current green is dull and flat.
- Motion must be clearly visible over ~20s while staying calm.

**2026-08-01T15:32:02Z**

Round 2 reviewed. Big step forward: rays and folds now exist and the geometric bunching works. Not accepted yet.

BLOCKER — the screenshots are useless for motion. aurora-r2-10s, -20s and -30s are pixel-identical, including the star twinkle, which is sin(time*1.7) and must change within one second. Virtual time is not advancing in the capture. Fix the capture before anything else: drive a real browser session over CDP (npx is available) and grab frames seconds apart on the wall clock, or add a temporary time override for capture only. Do not leave the override in the file. I cannot accept this ticket until I can see that the aurora moves.

Visual findings on round 2:

1. Far too bright and too saturated. It is neon. This is projected on a bedroom ceiling for sleep. Drop the peak brightness a lot and desaturate. The dim body matters more than the bright cores.
2. The top edge is a smooth scalloped boundary across the whole sash. It reads as an audio equalizer or a crown. Real rays feather out individually at many different heights with soft, indefinite ends. Add much more per-ray height variance at high spatial frequency and soften the upper fade so there is no shared silhouette.
3. The lower border is still a hard dark cut and still reads as a mountain ridge. In the reference photo the base is hidden behind real mountains; we have no mountains, so a crisp cut looks wrong. Fade the light out downward instead of terminating it.
4. The magenta appears as a vertical fringe on the left edge of bright rays, like chromatic aberration. Pink belongs at the TOP of a ray, not beside it.
5. The sash reads as separate solid bars on black. It needs a continuous dim body with brighter filaments inside it, so the bars belong to one sheet.
6. Some isolated tall thin bars float with nothing beneath them. They look like scratches on the lens.

Aim for: a soft, dim, continuous green sheet, brighter and denser near its lower part, dissolving into feathered rays toward the top, with a few brighter filaments. Calm, not dramatic.

**2026-08-01T15:35:49Z**

Round 3 reviewed. Motion verified — frames now differ properly. Thank you. Not accepted; the tone swung too far the other way.

What is wrong now:
1. The sheet is gone. The body is so dim that only a few isolated cores remain. Round 2 was too bright, round 3 is too dark. The body wants to sit around halfway between them.
2. The bright cores are razor-thin hard-edged lines, brightest along a 1-2 pixel line, and several have a hard edge on one side only. They read as light leaks or scanlines, not as light. This hard edge is now the single biggest tell that it is fake.
3. Fold bunching produces those razor lines instead of soft bright regions. Bunching must saturate into a soft glow.

Prescriptive design for round 4, since tuning alone is not converging. Draw the curtain in TWO additive passes over the same sample points:

  Pass A, the body: wide rays, roughly 12-20 low-res pixels of line width, low alpha, with a modest blur (about 3px at the offscreen scale). This is the continuous soft sheet and it should always be clearly visible.
  Pass B, the filaments: thin rays, roughly 3-6 low-res pixels, low alpha, with a small blur (about 1px). Keep the ray spacing larger than this blur so the filaments survive.

Both passes additive. The result is a soft sheet with soft-edged filaments inside it. No hard vertical edges anywhere in the image — that is the acceptance bar for this round.

Also:
- Clamp per-ray alpha so a tight fold sums into a soft bright region, not a line.
- Soften the vertical profile at the base so it does not terminate abruptly.
- Keep the individually feathered ray tops from round 3. Those are good.

Reference target: a soft dim green sheet, clearly present across its span, denser lower down, dissolving upward into feathered rays, with a few slightly brighter soft filaments.

**2026-08-01T15:41:07Z**

Round 4 reviewed. The hard edges are gone — that bar is met, and the two-pass structure is right. Keep it. Two remaining problems:

1. The filaments disappeared. The t step went from 0.0025 to 0.01, so there are only ~100 samples per curtain. At 16px body width the rays merge into a few blobs, and the 4px filaments are too sparse to read. Put the sample density back up so the body is genuinely continuous and the filaments are dense enough to see.
2. The colour is a dull grey-green and still too dim. Low alpha with a SATURATED hue gives dim but coloured light; low alpha with a desaturated hue gives grey. Raise saturation, keep alpha low.

Changing the loop. Tuning one variable per round is too slow. Produce a contact sheet of variants in one pass instead: a 3x3 grid over overall brightness (three levels) and filament strength/density (three levels), all with the round-4 two-pass structure and the higher sample density, captured at the same instant so only the tuning differs. I will pick a cell, or interpolate between cells, and then we are done with the look.

The variant harness is throwaway. It must not remain in index.html.

**2026-08-01T16:07:00Z**

Round 5 reviewed. Colour and softness are now right. Selected cell: brightness medium (0.55), filaments strong (strength 1.4, density 1.35). Make that the default.

One structural gap is left, and it is the last thing standing between this and a real aurora. Across all nine cells there are only TWO bright columns. A real aurora has dozens of visible striations along the whole sash. The filament brightness is evidently driven by the fold bunching, so only the two bunching knots light up and everything between them is flat haze.

Final changes:
1. Drive filament brightness mostly from per-ray high-frequency variation that is independent of the bunching, so distinct filaments appear along the WHOLE span. Let the bunching add on top of that rather than being the only source.
2. More folds. Increase the wobble so there are roughly four to six knots of varying strength instead of two.
3. The magenta top fringe reads grey-purple and muddy, and it is too wide. Make it narrower and warmer, closer to a faint pink rim than a purple haze.

This should be the last round on the look.

**2026-08-01T16:18:59Z**

Round 6 reviewed. Big improvement — filaments now run along the whole sash and this finally reads as an aurora. Two things left.

LOOK. It reads as an audio equalizer. About ten bars of very similar width, very similar spacing and a similar height envelope. Real aurora striations are highly irregular. Needed:
- Strong variance in filament width. Some should be two or three times wider than others.
- Irregular spacing. Not an even comb.
- A power-law-ish brightness distribution: many faint filaments, only a few bright ones. Right now most are about equally bright.
- More variance in height. Some rays should reach much higher than their neighbours.
- Bring back more of the continuous dim sheet between the filaments. They currently float as separate bars; the haze is what binds them into one curtain.

PERFORMANCE. Measured cost went from about 18ms per frame to about 44ms, so roughly 23fps. That is a real regression for something that runs all night. Get it back to comfortably under 16ms. Raising auroraScale is the cheapest lever and the blur hides the loss of resolution; reducing the sample count on the body pass is another, since the body is blurred anyway and does not need the same density as the filament pass. Measure, do not guess.

After this, the look is done and the ticket goes to code review.

**2026-08-01T16:27:35Z**

Round 7 reviewed. Irregularity is much better and the structure now reads as an aurora. Performance is fixed (7.5ms mean, 12.7ms max) — good.

Three items, then this is done.

1. LEFT-RIGHT SYMMETRY. This is the worst remaining artifact. The whole sash is close to mirror-symmetric about the vertical centre line, with a matching dark notch in the middle of every frame. Compare the bright filaments either side of centre in aurora-r7-02 and -1920x1080; they pair up. Something is symmetric — most likely the two curtains are placed as mirror images, or the end-fade envelope and the wobble phase happen to mirror. Break it. Give each curtain its own independent phase, span, offset and direction. Nature is not symmetric and the eye catches this immediately.

2. NO BRIGHT CORES. The power-law brightness overshot: everything is now faint. I asked for many faint and a FEW BRIGHT. Restore two or three genuinely bright filaments per frame while leaving the rest dim. The contrast between them is what sells it.

3. Slightly more binding haze between filaments, as in round 6. It is a little weak again.

Do not change anything else. Performance must stay under 16ms. After this the look is accepted and the ticket goes to code review.

**2026-08-01T16:37:24Z**

Look accepted at round 8: asymmetric, irregular, soft, calm, with a few brighter cores. Code review done by two reviewers.

Accepted for fixing now:
1. curtain.direction is not applied to three time terms (widthSignal, heightSignal, and the term inside rayHeight). Round 7 required each curtain to have an independent direction. Per-ray width and height therefore still evolve in the same temporal direction for both curtains — the exact correlation the symmetry fix was meant to remove. Must fix.
2. Cheap allocation wins only: hoist the constant curtains array out of draw, reuse a scratch ray buffer across frames instead of building ~268 objects per frame, and stop setting imageSmoothingEnabled every frame.
3. Remove the dead Math.min clamps on the gradient alphas. Both arguments are provably ordered, so they never clamp. Leftovers from a round when brightness could exceed 1.

Deliberately NOT doing: the CanvasGradient rework. Reviewers counted ~300 gradients and ~1800 RGBA strings per frame and this is the largest source of garbage, but reusing or approximating gradients changes the per-ray vertical profile, and the look took eight rounds to settle. Young-generation scavenges are cheap and there is no unbounded growth, no leak and no numerical drift over an all-night run — both reviewers confirmed that. Accepting bounded GC churn is the right trade against risking the visual. Revisit only if a real projector shows stutter.

Reviewers confirmed clean: no capture or debug scaffolding left in the file, no changes outside the aurora layer, no leaks, resize and degenerate viewports handled, no drift over hours.
