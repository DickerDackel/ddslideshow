import os.path

import bpy

from bpy.types import Operator, OperatorFileListElement
from bpy.props import StringProperty, CollectionProperty
from bpy_extras.io_utils import ImportHelper

from .utils import create_transform, crossfade, grep, load_image, apply_zoom

OP_PREFIX = 'ddslideshow'


def shit_i_cannot_figure_out_how_to_properly_call_load_images__from_create_slideshow(file_collection, directory, context):
    scene = context.scene
    ddslideshow = scene.ddslideshow
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

    files: CollectionProperty(name="File Path", type=OperatorFileListElement)
    directory: StringProperty(subtype='DIR_PATH', default='//')
    filename_ext = ""
    filter_glob: StringProperty(default='*.jpg;*.png;*.tif;*.tiff;*.bmp')

    def execute(self, context):
        def set_select(sequence, value):
            for strip in sequence:
                strip.select = value

        shit_i_cannot_figure_out_how_to_properly_call_load_images__from_create_slideshow(self.files, self.directory, context)

        set_select(bpy.context.scene.sequence_editor.sequences, False)
        set_select(grep(bpy.context.scene.sequence_editor.sequences, 'IMAGE'), True)
        bpy.ops.ddslideshow.overlap_images('INVOKE_DEFAULT')
        bpy.ops.ddslideshow.add_transforms('INVOKE_DEFAULT')

        set_select(bpy.context.scene.sequence_editor.sequences, False)
        set_select(grep(bpy.context.scene.sequence_editor.sequences, 'TRANSFORM'), True)
        bpy.ops.ddslideshow.zoom_transforms('INVOKE_DEFAULT')
        # bpy.ops.ddslideshow.pan_transforms('INVOKE_DEFAULT')

        set_select(bpy.context.scene.sequence_editor.sequences, False)
        set_select(grep(bpy.context.scene.sequence_editor.sequences, 'TRANSFORM'), True)
        bpy.ops.ddslideshow.crossfade('INVOKE_DEFAULT')

        set_select(bpy.context.scene.sequence_editor.sequences, False)
        bpy.ops.ddslideshow.slideshow_fade_in_out('INVOKE_DEFAULT')
        bpy.ops.ddslideshow.audio_fade_in_out('INVOKE_DEFAULT')

        return {'FINISHED'}

class SEQUENCE_EDITOR_OT_load_images(Operator, ImportHelper):
    bl_idname = f'{OP_PREFIX}.load_images'
    bl_label = 'Load images'


    # Configure ImportHelper
    files: CollectionProperty(name="File Path", type=OperatorFileListElement)
    directory: StringProperty(subtype='DIR_PATH', default='//')
    filename_ext = ""
    filter_glob: StringProperty(default='*.jpg;*.png;*.tif;*.tiff;*.bmp')

    def execute(self, context):
        shit_i_cannot_figure_out_how_to_properly_call_load_images__from_create_slideshow(self.files, self.directory, context)

        return {'FINISHED'}


class SEQUENCE_EDITOR_OT_overlap_images(Operator):
    bl_idname = f'{OP_PREFIX}.overlap_images'
    bl_label = 'Overlap images'

    @classmethod
    def poll(cls, context):
        if not context.selected_sequences: return False  # noqa: E701

        return all(strip.type == 'IMAGE' for strip in context.selected_sequences)

    def execute(self, context):
        scene = context.scene
        ddslideshow = scene.ddslideshow
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

        return {'FINISHED'}


class SEQUENCE_EDITOR_OT_add_transforms(Operator):
    bl_idname = f'{OP_PREFIX}.add_transforms'
    bl_label = 'Add transforms'

    @classmethod
    def poll(cls, context):
        if not context.selected_sequences: return False  # noqa: E701

        return all(strip.type == 'IMAGE' for strip in context.selected_sequences)

    def execute(self, context):
        for strip in context.selected_sequences:
            create_transform(strip)

        return {'FINISHED'}


class SEQUENCE_EDITOR_OT_zoom_transforms(Operator):
    bl_idname = f'{OP_PREFIX}.zoom_transforms'
    bl_label = 'Apply zoom'

    @classmethod
    def poll(cls, context):
        if not context.selected_sequences: return False  # noqa: E701

        return all(strip.type == 'TRANSFORM' for strip in context.selected_sequences)

    def execute(self, context):
        scene = context.scene
        ddslideshow = scene.ddslideshow

        intro = ddslideshow.intro
        outro = ddslideshow.outro
        zoom_from = ddslideshow.zoom_from
        zoom_to = ddslideshow.zoom_to
        zoom_random = ddslideshow.zoom_random

        seqs = context.selected_sequences
        seqlen = len(seqs)
        start = 1 if intro else 0
        end = seqlen - 1 if outro else seqlen

        for strip in seqs[start:end]:
            apply_zoom(strip, zoom_from, zoom_to, zoom_random)

        return {'FINISHED'}


class SEQUENCE_EDITOR_OT_pan_transforms(Operator):
    bl_idname = f'{OP_PREFIX}.pan_transforms'
    bl_label = 'Apply pan'

    @classmethod
    def poll(cls, context):
        if not context.selected_sequences: return False  # noqa: E701

        return all(strip.type == 'TRANSFORM' for strip in context.selected_sequences)

    def execute(self, context):
        scene = context.scene
        ddslideshow = scene.ddslideshow

        ...

        return {'FINISHED'}
        ...


class SEQUENCE_EDITOR_OT_crossfade(Operator):
    bl_idname = f'{OP_PREFIX}.crossfade'
    bl_label = 'Crossfade selection'

    @classmethod
    def poll(cls, context):
        return True  # FIXME
        return bool(context.selected_sequences)

    def execute(self, context):
        scene = context.scene
        ddslideshow = scene.ddslideshow
        fps = context.scene.render.fps

        slide_crossfade = ddslideshow.slide_crossfade * fps

        for strip1, strip2 in zip(context.selected_sequences, context.selected_sequences[1:]):
            crossfade(strip1, strip2, slide_crossfade)

        return {'FINISHED'}


class SEQUENCE_EDITOR_OT_slideshow_fade_in_out(Operator):
    bl_idname = f'{OP_PREFIX}.slideshow_fade_in_out'
    bl_label = 'Slideshow fade in/out'

    def execute(self, context):
        scene = context.scene
        ddslideshow = scene.ddslideshow
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
        scene = context.scene
        ddslideshow = scene.ddslideshow
        fps = context.scene.render.fps

        audio = ddslideshow.audio
        audio_fade_in = ddslideshow.slideshow_fade_in * fps
        audio_fade_out = ddslideshow.slideshow_fade_out * fps

        audio = context.scene.sequence_editor.sequences.new_sound(
            name=audio,
            filepath=audio,
            channel=6,
            frame_start=1)
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
