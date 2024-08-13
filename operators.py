import os.path

from random import choice
from itertools import cycle

import bpy

from bpy.types import Operator, OperatorFileListElement
from bpy.props import CollectionProperty, StringProperty
from bpy_extras.io_utils import ImportHelper

from .utils import (apply_pan, create_transform, crossfade,
                    deselect, grep, load_image, select,
                    image_filter, transform_filter)

OP_PREFIX = 'ddslideshow'


# If somebody could pretty please explain to me, how to properly call the
# load_images operator from create_slideshow?
def shit_i_cannot_figure_out_how_to_properly_call_load_images_from_create_slideshow(file_collection, directory, context):
    ddslideshow = context.scene.ddslideshow
    fps = context.scene.render.fps

    intro = bpy.path.abspath(ddslideshow.intro)
    outro = bpy.path.abspath(ddslideshow.outro)
    slide_duration = int(ddslideshow.slide_duration * fps)
    slide_crossfade = int(ddslideshow.slide_crossfade * fps)

    files = [os.path.join(directory, f.name) for f in file_collection]

    if os.path.isfile(intro):
        files.insert(0, intro)  # noqa: E701

    if os.path.isfile(outro):
        files.append(outro)  # noqa: E701

    full_duration = slide_duration + 2 * slide_crossfade
    images = [load_image(bpy.path.abspath(fname), 1 + i * full_duration, full_duration)
              for i, fname in enumerate(files)]

    context.scene.frame_end = images[-1].frame_final_end


class SEQUENCE_EDITOR_OT_create_slideshow(Operator, ImportHelper):
    bl_idname = f'{OP_PREFIX}.create_slideshow'
    bl_label = 'Run workflow'

    # Configure ImportHelper
    directory: StringProperty(subtype='DIR_PATH', default='//')
    files: CollectionProperty(name='File Path', type=OperatorFileListElement)
    filter_glob: StringProperty(default='*.jpg;*.png;*.tif;*.tiff;*.bmp')
    use_filter_image: True
    filename_ext = ''
    display_type = 'THUMBNAIL'

    def execute(self, context):
        ddslideshow = context.scene.ddslideshow
        has_intro = ddslideshow.intro not in ['', '//']
        has_outro = ddslideshow.outro not in ['', '//']

        shit_i_cannot_figure_out_how_to_properly_call_load_images_from_create_slideshow(self.files, self.directory, context)

        deselect(context.sequences)
        select(grep(image_filter, context.sequences))
        bpy.ops.ddslideshow.overlap_images('INVOKE_DEFAULT')

        bpy.ops.sequencer.view_all()

        deselect(context.sequences)
        select(grep(image_filter, context.sequences))
        bpy.ops.ddslideshow.add_transforms('INVOKE_DEFAULT')

        deselect(context.sequences)
        selected = list(grep(transform_filter, context.sequences))
        start = 1 if has_intro else 0
        end = -1 if has_outro else len(selected)
        select(selected[start:end])

        bpy.ops.ddslideshow.zoom_transforms('INVOKE_DEFAULT')
        bpy.ops.ddslideshow.pan_transforms('INVOKE_DEFAULT')

        deselect(context.sequences)
        select(grep(transform_filter, context.sequences))
        bpy.ops.ddslideshow.crossfade('INVOKE_DEFAULT')

        deselect(context.sequences)
        bpy.ops.ddslideshow.slideshow_fade_in_out('INVOKE_DEFAULT')

        if bpy.ops.ddslideshow.audio_fade_in_out.poll():
            bpy.ops.ddslideshow.audio_fade_in_out('INVOKE_DEFAULT')

        return {'FINISHED'}

class SEQUENCE_EDITOR_OT_load_images(Operator, ImportHelper):
    bl_idname = f'{OP_PREFIX}.load_images'
    bl_label = 'Load images'

    # Configure ImportHelper
    directory: StringProperty(subtype='DIR_PATH', default='//')
    files: CollectionProperty(name='File Path', type=OperatorFileListElement)
    filter_glob: StringProperty(default='*.jpg;*.png;*.tif;*.tiff;*.bmp')
    use_filter_image: True
    filename_ext = ''
    display_type = 'THUMBNAIL'

    def execute(self, context):
        shit_i_cannot_figure_out_how_to_properly_call_load_images_from_create_slideshow(self.files, self.directory, context)
        select(grep(image_filter, context.sequences))

        bpy.ops.sequencer.view_all()

        return {'FINISHED'}


class SEQUENCE_EDITOR_OT_overlap_images(Operator):
    bl_idname = f'{OP_PREFIX}.overlap_images'
    bl_label = 'Overlap images'

    @classmethod
    def poll(cls, context):
        selected = context.selected_sequences

        return (selected
                and all(strip.type == 'IMAGE' for strip in selected))

    def execute(self, context):
        ddslideshow = context.scene.ddslideshow
        fps = context.scene.render.fps

        slide_duration = int(ddslideshow.slide_duration * fps)
        slide_crossfade = int(ddslideshow.slide_crossfade * fps)

        fps = context.scene.render.fps

        # Could probably be done with one expression when iterating from the
        # end, but this seems clearer.

        # First doesn't get left slide_crossfade
        images = context.selected_sequences
        images[0].frame_final_duration = slide_duration + slide_crossfade

        for prev, this in zip(images, images[1:-1]):
            this.frame_start = prev.frame_final_end - slide_crossfade
            this.frame_final_duration = slide_duration + 2 * slide_crossfade

        # Last doesn't get right slide_crossfade
        images[-1].frame_start = images[-2].frame_final_end - slide_crossfade
        images[-1].frame_final_duration = slide_duration + slide_crossfade

        context.scene.frame_end = images[-1].frame_final_end

        bpy.ops.sequencer.view_all()

        return {'FINISHED'}


class SEQUENCE_EDITOR_OT_add_transforms(Operator):
    bl_idname = f'{OP_PREFIX}.add_transforms'
    bl_label = 'Add transforms'

    @classmethod
    def poll(cls, context):
        selected = context.selected_sequences

        return (selected
                and all(strip.type == 'IMAGE' for strip in selected))

    def execute(self, context):
        for strip in context.selected_sequences:
            create_transform(strip)

        select(grep(transform_filter, context.sequences))

        return {'FINISHED'}


class SEQUENCE_EDITOR_OT_zoom_transforms(Operator):
    bl_idname = f'{OP_PREFIX}.zoom_transforms'
    bl_label = 'Apply zoom'

    @classmethod
    def poll(cls, context):
        selected = context.selected_sequences

        return (selected
                and all(strip.type == 'TRANSFORM' for strip in selected))

    def execute(self, context):
        scene = bpy.context.scene
        ddslideshow = scene.ddslideshow

        # setting the value anywhere in the timeline somehow supresses the
        # calculation of the proper position between keyframes and makes the
        # image jump at that one frame.  So we need to position the current
        # frame to the place where we set the value.  Frame position is reset
        # when the function is finished.
        current_frame = scene.frame_current

        zoom_from = ddslideshow.zoom_from
        zoom_to = ddslideshow.zoom_to
        zoom_randomize = ddslideshow.zoom_randomize

        for strip in context.selected_sequences:
            if zoom_randomize:
                zoom = choice(((zoom_from, zoom_to),
                               (zoom_to, zoom_from)))
            else:
                zoom = (zoom_from, zoom_to)

            scene.frame_set(strip.frame_final_start)
            strip.scale_start_x = strip.scale_start_y = zoom[0]
            strip.keyframe_insert(data_path='scale_start_x', frame=strip.frame_final_start)
            strip.keyframe_insert(data_path='scale_start_y', frame=strip.frame_final_start)

            scene.frame_set(strip.frame_final_end)
            strip.scale_start_x = strip.scale_start_y = zoom[1]
            strip.keyframe_insert(data_path='scale_start_x', frame=strip.frame_final_end)
            strip.keyframe_insert(data_path='scale_start_y', frame=strip.frame_final_end)

            # Store the randomized values as attributes in the stripo, since I
            # no idea to get the keyframe data out again
            strip['zoom_from'] = zoom[0]
            strip['zoom_to'] = zoom[1]

        scene.frame_set(current_frame)
        return {'FINISHED'}


class SEQUENCE_EDITOR_OT_pan_transforms(Operator):
    bl_idname = f'{OP_PREFIX}.pan_transforms'
    bl_label = 'Apply pan'

    @classmethod
    def poll(cls, context):
        selected = context.selected_sequences

        return (selected
                and all(strip.type == 'TRANSFORM' for strip in selected)
                and all('zoom_from' in strip for strip in selected)
                and all('zoom_to' in strip for strip in selected))

    def execute(self, context):
        ddslideshow = context.scene.ddslideshow

        pan_config = ddslideshow.pan

        selected = context.selected_sequences
        slen = len(selected)

        pan_directions = {'nw': (1, -1), 'n': (0, -1), 'ne': (-1, -1),
                          'w': (1, 0), '0': (0, 0), 'e': (-1, 0),
                          'sw': (1, 1), 's': (0, 1), 'se': (-1, 1)}
        cw = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']
        ccw = reversed(cw)

        if pan_config == 'off':
            positions = [pan_directions['0'] for _ in range(slen)]
        elif pan_config == 'randomize':
            directions = list(pan_directions.values())
            positions = [choice(directions) for _ in range(slen)]
        elif pan_config == 'cw':
            positions = [pan_directions[key] for key, _ in zip(cycle(cw), range(slen))]
        elif pan_config == 'ccw':
            positions = [pan_directions[key] for key, _ in zip(cycle(ccw), range(slen))]
        elif pan_config in pan_directions:
            positions = [pan_directions[pan_config] for _ in  range(slen)]

        for strip, (dx, dy) in zip(selected, positions):
            apply_pan(strip, dx, dy, strip['zoom_from'], strip['zoom_to'])

        return {'FINISHED'}


class SEQUENCE_EDITOR_OT_crossfade(Operator):
    bl_idname = f'{OP_PREFIX}.crossfade'
    bl_label = 'Crossfade selection'

    @classmethod
    def poll(cls, context):
        return bool(context.selected_sequences)

    def execute(self, context):
        ddslideshow = context.scene.ddslideshow
        fps = context.scene.render.fps

        slide_crossfade = ddslideshow.slide_crossfade * fps

        for strip1, strip2 in zip(context.selected_sequences, context.selected_sequences[1:]):
            crossfade(strip1, strip2, slide_crossfade)

        return {'FINISHED'}


class SEQUENCE_EDITOR_OT_slideshow_fade_in_out(Operator):
    bl_idname = f'{OP_PREFIX}.slideshow_fade_in_out'
    bl_label = 'Slideshow fade in/out'

    def execute(self, context):
        ddslideshow = context.scene.ddslideshow
        fps = context.scene.render.fps

        slideshow_fade_in = ddslideshow.slideshow_fade_in * fps
        slideshow_fade_out = ddslideshow.slideshow_fade_out * fps

        adjustment = context.scene.sequence_editor.sequences.new_effect(
            type='ADJUSTMENT',
            name='fade-in-out',
            channel=6,
            frame_start = 0,
            frame_end = context.scene.frame_end)

        adjustment.color_multiply = 0
        adjustment.keyframe_insert(data_path='color_multiply', frame=0)
        adjustment.color_multiply = 1
        adjustment.keyframe_insert(data_path='color_multiply', frame=slideshow_fade_in)
        adjustment.color_multiply = 1
        adjustment.keyframe_insert(data_path='color_multiply', frame=adjustment.frame_final_end - slideshow_fade_out)
        adjustment.color_multiply = 0
        adjustment.keyframe_insert(data_path='color_multiply', frame=adjustment.frame_final_end)

        return {'FINISHED'}


class SEQUENCE_EDITOR_OT_audio_fade_in_out(Operator):
    bl_idname = f'{OP_PREFIX}.audio_fade_in_out'
    bl_label = 'Add audio'

    @classmethod
    def poll(cls, context):
        return context.scene.ddslideshow.audio != ''

    def execute(self, context):
        ddslideshow = context.scene.ddslideshow
        fps = context.scene.render.fps

        audio = ddslideshow.audio
        audio_fade_in = ddslideshow.slideshow_fade_in * fps
        audio_fade_out = ddslideshow.slideshow_fade_out * fps

        audio = context.scene.sequence_editor.sequences.new_sound(
            name=audio,
            filepath=audio,
            channel=7,
            frame_start=1)
        if audio.frame_final_end > context.scene.frame_end:
            audio.frame_final_end = context.scene.frame_end

        audio.volume = 0
        audio.keyframe_insert(data_path='volume', frame=1)
        audio.volume = 1
        audio.keyframe_insert(data_path='volume', frame=audio_fade_in)
        audio.volume = 1
        audio.keyframe_insert(data_path='volume', frame=audio.frame_final_end - audio_fade_out)
        audio.volume = 0
        audio.keyframe_insert(data_path='volume', frame=audio.frame_final_end)

        return {'FINISHED'}


class SEQUENCE_EDITOR_OT_pan_base(Operator):
    @classmethod
    def poll(cls, context):
        selected = context.selected_sequences

        # return (selected and all(strip.type == 'TRANSFORM' for strip in selected))
        return (selected
                and all(strip.type == 'TRANSFORM' for strip in selected)
                and all('zoom_from' in strip for strip in selected)
                and all('zoom_to' in strip for strip in selected))

class SEQUENCE_EDITOR_OT_pan_start_nw(SEQUENCE_EDITOR_OT_pan_base):
    bl_idname = f'{OP_PREFIX}.pan_start_nw'
    bl_label = 'NW'
    def execute(self, context):
        self.report({'INFO'}, 'Start nw called')
        return {'FINISHED'}

class SEQUENCE_EDITOR_OT_pan_start_n(SEQUENCE_EDITOR_OT_pan_base):
    bl_idname = f'{OP_PREFIX}.pan_start_n'
    bl_label = 'N'
    def execute(self, context):
        self.report({'INFO'}, 'Start n called')
        return {'FINISHED'}

class SEQUENCE_EDITOR_OT_pan_start_ne(SEQUENCE_EDITOR_OT_pan_base):
    bl_idname = f'{OP_PREFIX}.pan_start_ne'
    bl_label = 'NE'
    def execute(self, context):
        self.report({'INFO'}, 'Start ne called')
        return {'FINISHED'}

class SEQUENCE_EDITOR_OT_pan_start_w(SEQUENCE_EDITOR_OT_pan_base):
    bl_idname = f'{OP_PREFIX}.pan_start_w'
    bl_label = 'W'
    def execute(self, context):
        self.report({'INFO'}, 'Start w called')
        return {'FINISHED'}

class SEQUENCE_EDITOR_OT_pan_start_0(SEQUENCE_EDITOR_OT_pan_base):
    bl_idname = f'{OP_PREFIX}.pan_start_0'
    bl_label = '0'
    def execute(self, context):
        self.report({'INFO'}, 'Start 0 called')
        return {'FINISHED'}

class SEQUENCE_EDITOR_OT_pan_start_e(SEQUENCE_EDITOR_OT_pan_base):
    bl_idname = f'{OP_PREFIX}.pan_start_e'
    bl_label = 'E'
    def execute(self, context):
        self.report({'INFO'}, 'Start e called')
        return {'FINISHED'}

class SEQUENCE_EDITOR_OT_pan_start_sw(SEQUENCE_EDITOR_OT_pan_base):
    bl_idname = f'{OP_PREFIX}.pan_start_sw'
    bl_label = 'SW'
    def execute(self, context):
        self.report({'INFO'}, 'Start sw called')
        return {'FINISHED'}

class SEQUENCE_EDITOR_OT_pan_start_s(SEQUENCE_EDITOR_OT_pan_base):
    bl_idname = f'{OP_PREFIX}.pan_start_s'
    bl_label = 'S'
    def execute(self, context):
        self.report({'INFO'}, 'Start s called')
        return {'FINISHED'}

class SEQUENCE_EDITOR_OT_pan_start_se(SEQUENCE_EDITOR_OT_pan_base):
    bl_idname = f'{OP_PREFIX}.pan_start_se'
    bl_label = 'SE'
    def execute(self, context):
        self.report({'INFO'}, 'Start se called')
        return {'FINISHED'}

class SEQUENCE_EDITOR_OT_pan_start_random(SEQUENCE_EDITOR_OT_pan_base):
    bl_idname = f'{OP_PREFIX}.pan_start_random'
    bl_label = 'Random'
    def execute(self, context):
        self.report({'INFO'}, 'Random called')
        return {'FINISHED'}

class SEQUENCE_EDITOR_OT_pan_start_cw(SEQUENCE_EDITOR_OT_pan_base):
    bl_idname = f'{OP_PREFIX}.pan_start_cw'
    bl_label = 'CW'
    def execute(self, context):
        self.report({'INFO'}, 'CW called')
        return {'FINISHED'}

class SEQUENCE_EDITOR_OT_pan_start_ccw(SEQUENCE_EDITOR_OT_pan_base):
    bl_idname = f'{OP_PREFIX}.pan_start_ccw'
    bl_label = 'CCW'
    def execute(self, context):
        self.report({'INFO'}, 'CCW called')
        return {'FINISHED'}

class SEQUENCE_EDITOR_OT_pan_end_nw(SEQUENCE_EDITOR_OT_pan_base):
    bl_idname = f'{OP_PREFIX}.pan_end_nw'
    bl_label = 'NW'
    def execute(self, context):
        self.report({'INFO'}, 'end nw called')
        return {'FINISHED'}

class SEQUENCE_EDITOR_OT_pan_end_n(SEQUENCE_EDITOR_OT_pan_base):
    bl_idname = f'{OP_PREFIX}.pan_end_n'
    bl_label = 'N'
    def execute(self, context):
        self.report({'INFO'}, 'end n called')
        return {'FINISHED'}

class SEQUENCE_EDITOR_OT_pan_end_ne(SEQUENCE_EDITOR_OT_pan_base):
    bl_idname = f'{OP_PREFIX}.pan_end_ne'
    bl_label = 'NE'
    def execute(self, context):
        self.report({'INFO'}, 'end ne called')
        return {'FINISHED'}

class SEQUENCE_EDITOR_OT_pan_end_w(SEQUENCE_EDITOR_OT_pan_base):
    bl_idname = f'{OP_PREFIX}.pan_end_w'
    bl_label = 'W'
    def execute(self, context):
        self.report({'INFO'}, 'end w called')
        return {'FINISHED'}

class SEQUENCE_EDITOR_OT_pan_end_0(SEQUENCE_EDITOR_OT_pan_base):
    bl_idname = f'{OP_PREFIX}.pan_end_0'
    bl_label = '0'
    def execute(self, context):
        self.report({'INFO'}, 'end 0 called')
        return {'FINISHED'}

class SEQUENCE_EDITOR_OT_pan_end_e(SEQUENCE_EDITOR_OT_pan_base):
    bl_idname = f'{OP_PREFIX}.pan_end_e'
    bl_label = 'E'
    def execute(self, context):
        self.report({'INFO'}, 'end e called')
        return {'FINISHED'}

class SEQUENCE_EDITOR_OT_pan_end_sw(SEQUENCE_EDITOR_OT_pan_base):
    bl_idname = f'{OP_PREFIX}.pan_end_sw'
    bl_label = 'SW'
    def execute(self, context):
        self.report({'INFO'}, 'end sw called')
        return {'FINISHED'}

class SEQUENCE_EDITOR_OT_pan_end_s(SEQUENCE_EDITOR_OT_pan_base):
    bl_idname = f'{OP_PREFIX}.pan_end_s'
    bl_label = 'S'
    def execute(self, context):
        self.report({'INFO'}, 'end s called')
        return {'FINISHED'}

class SEQUENCE_EDITOR_OT_pan_end_se(SEQUENCE_EDITOR_OT_pan_base):
    bl_idname = f'{OP_PREFIX}.pan_end_se'
    bl_label = 'SE'
    def execute(self, context):
        self.report({'INFO'}, 'end se called')
        return {'FINISHED'}

class SEQUENCE_EDITOR_OT_pan_end_random(SEQUENCE_EDITOR_OT_pan_base):
    bl_idname = f'{OP_PREFIX}.pan_end_random'
    bl_label = 'Random'
    def execute(self, context):
        self.report({'INFO'}, 'Random called')
        return {'FINISHED'}

class SEQUENCE_EDITOR_OT_pan_end_cw(SEQUENCE_EDITOR_OT_pan_base):
    bl_idname = f'{OP_PREFIX}.pan_end_cw'
    bl_label = 'CW'
    def execute(self, context):
        self.report({'INFO'}, 'CW called')
        return {'FINISHED'}

class SEQUENCE_EDITOR_OT_pan_end_ccw(SEQUENCE_EDITOR_OT_pan_base):
    bl_idname = f'{OP_PREFIX}.pan_end_ccw'
    bl_label = 'CCW'
    def execute(self, context):
        self.report({'INFO'}, 'CCW called')
        return {'FINISHED'}
