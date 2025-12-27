===
outpaint-resize: file, py
===
Outpaint a thin border to fill bleed areas.

@image: load-rgb
@canvas: expand-by 21px
@canvas: step-zoom 7, LANCZOS
@edge: blur-blend 3, overlap 1px
@cli: --targets
