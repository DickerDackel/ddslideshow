## Operators

1. Load images
1. Overlap images
1. Add transforms
    - Zoom images
    - Pan images
1. Crossfade selection
1. Fade in/out slideshow (Adjustment layer)
1. Load audiotrack
1. Fade in/out audiotrack

## Properties

1. Slide duration
1. Slide crossfade
1. Zoom
    - start frame
    - end frame
    - randomize order
1. Pan
    - direction (9-way box, random, cw, ccw)
    - amount or auto?
1. Slideshow fade in/out
    - in duration
    - out duration
1. Audiotrack fade in/out
    - in duration
    - out duration

## Behaviour

Pan size < 1 always centered
Pan size > 1 always anchored at direction

distance = 100 * (zoom - 1) / 2
first direction = -direction
