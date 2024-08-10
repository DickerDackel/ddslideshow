from os.path import basename
from random import choice

import bpy


def grep(sequence, type_):
    return (strip for strip in sequence if strip.type == type_)


def load_image(fname, frame, length):
    image = bpy.context.scene.sequence_editor.sequences.new_image(
        name=basename(fname),
        filepath=fname,
        channel=0,
        frame_start=frame,
        fit_method='ORIGINAL')
    image.frame_final_end = frame + length

    return image


def create_transform(strip):
    return bpy.context.scene.sequence_editor.sequences.new_effect(
        type='TRANSFORM',
        name=f'trns-{strip.name}',
        channel=strip.channel + 2,
        seq1=strip,
        frame_start=strip.frame_final_start)


def apply_zoom(strip, zoom_from=1.0, zoom_to=1.5, randomize=False):
    if randomize:
        zoom = choice(((zoom_from, zoom_to),
                       (zoom_to, zoom_from)))
    else:
        zoom = (zoom_from, zoom_to)

    strip.scale_start_x = strip.scale_start_y = zoom[0]
    strip.keyframe_insert(data_path='scale_start_x', frame=strip.frame_final_start)
    strip.keyframe_insert(data_path='scale_start_y', frame=strip.frame_final_start)

    strip.scale_start_x = strip.scale_start_y = zoom[1]
    strip.keyframe_insert(data_path='scale_start_x', frame=strip.frame_final_end)
    strip.keyframe_insert(data_path='scale_start_y', frame=strip.frame_final_end)


def crossfade(strip1, strip2, duration):
    return bpy.context.scene.sequence_editor.sequences.new_effect(
        type='GAMMA_CROSS',
        name=f'crossfade-{strip1.name}',
        channel=max(strip1.channel, strip2.channel) + 1,
        seq1=strip1,
        seq2=strip2,
        frame_start=strip2.frame_final_start,
        frame_end=strip1.frame_final_end)


def fade_in_out(adjustment, duration):
    print(adjustment)
    start = adjustment.frame_final_start
    end = adjustment.frame_final_end

    adjustment.color_multiply = 0
    adjustment.keyframe_insert(data_path='color_multiply', frame=0)
    adjustment.color_multiply = 1
    adjustment.keyframe_insert(data_path='color_multiply', frame=duration)
    adjustment.color_multiply = 1
    adjustment.keyframe_insert(data_path='color_multiply', frame=end - duration)
    adjustment.color_multiply = 0
    adjustment.keyframe_insert(data_path='color_multiply', frame=end)
