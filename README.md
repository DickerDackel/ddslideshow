# ddslideshow - Create Ken Burns Effect slideshow

## Slideshow creation

### Preparation

1. Create a new project
2. Switch to the Video Editing
3. Open the DDSlideshow panel on the right side of the timeline

The default setting will give you a slideshow without intro or outro slides,
no music, a random zoom in or out with a scale between 1.0 and 1.5, and
panning in a random 8-way direction.

- Optionally load intro and outro slides, e.g. with your studio logo
- Optionally load an audio track
- Configure the range of zooming.
- Configure the direction of panning.

See **Settings** further down this document for details.

### Simple workflow

Click "Run all", which will open a file browser.  Select all images for the
slideshow.  (In contrast to how other file browsers work, shift- or
control-click won't work as expected with Blender.  Either filter filenames at
the bottom input with a wildcard, or use [shift] B, which will allow you to
box select files.

Confirm the dialog and a finished slideshow with all configured settings from
above will be created.

You can click the play button below the timeline window to preview it.

### Manual workflow

Instead of "Run all", you can also follow the individual steps in the workflow
tab.

Note: Some workflow steps depend on a proper selection of strips. The
individual workflow steps try to set a usable selection, e.g. all images after
the image loading, but you might want to modify this selection.

**Load images** opens the same file browser as in the `Run all` workflow.

**Overlap images** applies the `Slide duration` and `Slide crossfade` settings
to the selected images.

**Add transforms** adds transform strips for each selected image.

**Apply zoom** adds zoom to all selected transform strips.  You might want to
deselect the transforms for the intro and outro slide.  The Simple generation
workflow will do that automatically for you.

**Apply pan** will do exactly that.  There are some rules for panning, and it
is dependent of the zoom settings.  See Settings below.  It's best to leave
the intro and outro strips deselected here as well.

**Add crossfade** will crossfade images or transforms, depending on the
selection.  It makes no sense to crossfade the images, when the transform is
on top of them.  So the Simple generation workflow will select all transform
strips automatically.

If you're selecting the strips manually, you might now want to add the intro
and outro strips again in your selection.

**Slideshow fade in/out** will add a adjustment strip to fade the slideshow in
from black at the beginning, and to black at the end.

**Audio fade in/out** will load the audio track and fade it in and out
according to the configured durations at the beginning and end.

If the audio track is longer than the slideshow, it will be shortened and the
configured fade out will be applied at the end of the slideshow instead of the
end of the track.

Note, that this script has no way do deal with an audio strip that is shorter
than the slide show.  The options to manually deal with that are:

- Accept the silence until the end of the slideshow
- Provide an audio track with a sufficient length
- Duplicate the audio track, shift it towards the end of the first track and
  make them blend into each other.  In this case, fading the end out also
  needs to be done manually.

### Fine tuning

Since this script doesn't know anything about the point of interest in an
image, the global settings for zooming and panning might not be adequate for
every image.  Both settings can be modified after the creation of the slide
show.

To do this, scroll through the timeline and find images where you want to
change the zoom direction or the pan anchor.  Then select that specific image,
configure zoom or pan and press `Apply zoom` or `Apply pan` again for this
single selected image.

Note, since the calculation of the panning depends on the zoom, panning also
needs to be re-applied when the zoom is changed.

Repeat this until you're happy with the whole slideshow.

### Exporting

Finally render the slide show into a movie.

If you're familiar with Blender, you might already have configured your
prefered export settings yourself, but in case you're not, here are some sane
defaults:


The output is configured in the top right corner at the printer icon.

- In the Format heading, select `HDTV 1080p`.
- Leave the framerate at 24 fps
- `Frame end` should be configured automatically by the slideshow generation
- After saving the project, type `//your-project-name` into the output. This
  will export to the same directory the project's `.blend` file is saved in.
- Set the file format to `FFmpeg Video`
- Below `Encoding`, set Container to `mpeg-4`.
- The `H.264` video codec should be good.
- Audio is set to `No Audio` by default.  Set it to either `AAC` or `mp3`.

Then save your project again, so no settings can get lost.

Finally export with Render -> Render Animation from the top bar, or by
pressing Ctrl-F12.

## Settings

### Media

**intro**, **outro** are image slides that will be placed before and after the
actual slideshow.  Place your studio logo here, or a slide with descriptive
text.

**audio** is a music or voice track to accompany the slideshow

### Global settings

**Slideshow fade in/out** gives the time for the fade in and out effect at the
beginning and end of the slideshow.

**Audio fade in/out** configures the same for the audio track.

### Per slide settings

**duration** is the duration that any slide will be shown unobstrued.
Crossfading slides is not included in this duration.

**crossfade** is the duration that 2 images will blend into each other.

The defaults for both should be fine to showcase all images without lingering
too long.

**zoom from**, **zoom to** configure the amount of zooming.  The image will zoom
kkfrom a scale of `zoom from` to a scale of `zoom to` by default.  If you want a
zoom out, just switch the values.  The default will zoom from an unscaled
image to a scale of 1.5.

**Randomize zoom direction** will randomly switch between zooming in or out for
each slide.

**Pan** will select the direction of the panning.

**Off** - No panning

**NW**, **N**, **NE**,
**W**,  **0**, **E**,
**SW**, **S**, **SE** are anchor points that the image will pan towards.

**Randomize** will select a random direction from above for every slide.

**Clockwise**, **Counter clockwise** will cycle through the anchors in the
given direction, starting with **N**.

The behaviour of panning is dependent of the zoom settings

- A zoom of 1 will disable both zooming and panning.
- A zoom <= 1 will always anchor the pan at the center of the screen
- A zoom > 1 will pan the image towards the configured anchor direction.

## Installation

The addon is packaged in the new plugin format that came with the Blender
4.2 release.

In this early stage, it's not yet registered on the blender add-ons site, but
that will happen a few tests and a bit of auditing down the road.

So currently, either download the release or clone the github repo to create
the package yourself.

### Download the release package

Download the latest version from the github release page here:

https://github.com/DickerDackel/ddslideshow/releases

Go to Edit -> Preferences -> Get Extensions

Click the arrow in the top right and at the bottom of the menu "Install from
disk".

DDslideshow should then appear in the Add-Ons page and already be activated.

### Clone the github repo

```bash
git clone https://github.com/dickerdackel/ddslideshow
cd ddslideshow
blender --command extension build
```

After that, there will be a zip file ddslideshow-VERSION.zip in the same
directory.  You can install that the same as the release package described
above.

## License

MIT License

Copyright (c) 2024 Michael Lamertz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
