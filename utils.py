from os.path import basename
from random import choice

import bpy


def grep(sequence, type_):
    return (strip for strip in sequence if strip.type == type_)


def load_image(fname, frame, length):
    name = basename(fname)
    image = bpy.context.scene.sequence_editor.sequences.new_image(
        name=name,
        filepath=fname,
        channel=0,
        frame_start=frame,
        fit_method='ORIGINAL')
    image.frame_final_end = frame + length

    return image


def create_transform(strip):
    name = f'dds-translate-{strip.name}'
    return bpy.context.scene.sequence_editor.sequences.new_effect(
        type='TRANSFORM',
        name=name,
        channel=strip.channel + 2,
        seq1=strip,
        frame_start=strip.frame_final_start)


def apply_zoom(strip, zoom_from=1.0, zoom_to=1.5, randomize=False):
    if randomize:
        zoom = choice(((zoom_from, zoom_to),
                       (zoom_to, zoom_from)))
    else:
        zoom = (zoom_from, zoom_to)

    # setting the value anywhere in the timeline somehow supresses the
    # calculation of the proper position between keyframes and makes the image
    # jump at that one frame.  So we need to position the current frame to the
    # place where we set the value.  Frame position is reset when the function
    # is finished.
    scene = bpy.context.scene
    current_frame = scene.frame_current

    scene.frame_set(strip.frame_final_start)
    strip.scale_start_x = strip.scale_start_y = zoom[0]
    strip.keyframe_insert(data_path='scale_start_x', frame=strip.frame_final_start)
    strip.keyframe_insert(data_path='scale_start_y', frame=strip.frame_final_start)

    scene.frame_set(strip.frame_final_end)
    strip.scale_start_x = strip.scale_start_y = zoom[1]
    strip.keyframe_insert(data_path='scale_start_x', frame=strip.frame_final_end)
    strip.keyframe_insert(data_path='scale_start_y', frame=strip.frame_final_end)

    scene.frame_set(current_frame)

    # Make this accessible for panning, since I have no idea to get the
    # keyframe data out again
    strip['zoom_from'] = zoom[0]
    strip['zoom_to'] = zoom[1]


def apply_pan(strip, dx, dy, zoom_from, zoom_to):
    def pan_and_keyframe(dx, dy, scale, frame):
        # Images smaller than the screen pan towards the center
        if scale <= 1:
            pos_x = pos_y = 0
        else:
            percent = (scale - 1) * 100 / 2
            pos_x = dx * percent
            pos_y = dy * percent

        strip.translate_start_x = pos_x
        strip.translate_start_y = pos_y
        strip.keyframe_insert(data_path='translate_start_x', frame=frame)
        strip.keyframe_insert(data_path='translate_start_y', frame=frame)


    # See comment above in apply_zoom
    scene = bpy.context.scene
    current_frame = scene.frame_current

    scene.frame_set(strip.frame_final_start)
    pan_and_keyframe(-dx, -dy, zoom_from, strip.frame_final_start)

    scene.frame_set(strip.frame_final_end)
    pan_and_keyframe(dx, dy, zoom_to, strip.frame_final_end)

    scene.frame_set(current_frame)


def crossfade(strip1, strip2, duration):
    clean_name = strip1.name.removeprefix('dds-translate')
    name = f'dds-crossfade-{clean_name}'
    return bpy.context.scene.sequence_editor.sequences.new_effect(
        type='GAMMA_CROSS',
        name=name,
        channel=max(strip1.channel, strip2.channel) + 1,
        seq1=strip1,
        seq2=strip2,
        frame_start=strip2.frame_final_start,
        frame_end=strip1.frame_final_end)


def fade_in_out(adjustment, duration):
    end = adjustment.frame_final_end

    adjustment.color_multiply = 0
    adjustment.keyframe_insert(data_path='color_multiply', frame=0)
    adjustment.color_multiply = 1
    adjustment.keyframe_insert(data_path='color_multiply', frame=duration)
    adjustment.color_multiply = 1
    adjustment.keyframe_insert(data_path='color_multiply', frame=end - duration)
    adjustment.color_multiply = 0
    adjustment.keyframe_insert(data_path='color_multiply', frame=end)
