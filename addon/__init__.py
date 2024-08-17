import bpy

from .properties import DDSlideshowProperties
from .panel import (SEQUENCE_EDITOR_PT_run_all,
                    SEQUENCE_EDITOR_PT_run_workflow,
                    SEQUENCE_EDITOR_PT_media,
                    SEQUENCE_EDITOR_PT_per_slide,
                    SEQUENCE_EDITOR_PT_zoom_pan_settings,
                    SEQUENCE_EDITOR_PT_transitions)
from .operators import (SEQUENCE_EDITOR_OT_run_workflow,
                        SEQUENCE_EDITOR_OT_load_images,
                        SEQUENCE_EDITOR_OT_overlap_images,
                        SEQUENCE_EDITOR_OT_add_transforms,
                        SEQUENCE_EDITOR_OT_zoom_transforms,
                        SEQUENCE_EDITOR_OT_switch_zooms,
                        SEQUENCE_EDITOR_OT_pan_transforms,
                        SEQUENCE_EDITOR_OT_crossfade,
                        SEQUENCE_EDITOR_OT_slideshow_fade_in_out,
                        SEQUENCE_EDITOR_OT_audio_fade_in_out,
                        SEQUENCE_EDITOR_OT_pan_start_nw, SEQUENCE_EDITOR_OT_pan_start_n, SEQUENCE_EDITOR_OT_pan_start_ne,
                        SEQUENCE_EDITOR_OT_pan_start_w, SEQUENCE_EDITOR_OT_pan_start_0, SEQUENCE_EDITOR_OT_pan_start_e,
                        SEQUENCE_EDITOR_OT_pan_start_sw, SEQUENCE_EDITOR_OT_pan_start_s, SEQUENCE_EDITOR_OT_pan_start_se,
                        SEQUENCE_EDITOR_OT_pan_end_nw, SEQUENCE_EDITOR_OT_pan_end_n, SEQUENCE_EDITOR_OT_pan_end_ne,
                        SEQUENCE_EDITOR_OT_pan_end_w, SEQUENCE_EDITOR_OT_pan_end_0, SEQUENCE_EDITOR_OT_pan_end_e,
                        SEQUENCE_EDITOR_OT_pan_end_sw, SEQUENCE_EDITOR_OT_pan_end_s, SEQUENCE_EDITOR_OT_pan_end_se,
                        SEQUENCE_EDITOR_OT_pan_random, SEQUENCE_EDITOR_OT_pan_cw, SEQUENCE_EDITOR_OT_pan_ccw,
                        SEQUENCE_EDITOR_OT_align_images, SEQUENCE_EDITOR_OT_align_images_center,
                        SEQUENCE_EDITOR_OT_align_images_top, SEQUENCE_EDITOR_OT_align_images_bottom,
                        SEQUENCE_EDITOR_OT_align_images_left, SEQUENCE_EDITOR_OT_align_images_right)


classes = [
    DDSlideshowProperties,
    SEQUENCE_EDITOR_PT_run_all,
    SEQUENCE_EDITOR_PT_run_workflow,
    SEQUENCE_EDITOR_PT_media,
    SEQUENCE_EDITOR_PT_per_slide,
    SEQUENCE_EDITOR_PT_zoom_pan_settings,
    SEQUENCE_EDITOR_PT_transitions,
    SEQUENCE_EDITOR_OT_run_workflow,
    SEQUENCE_EDITOR_OT_load_images,
    SEQUENCE_EDITOR_OT_overlap_images,
    SEQUENCE_EDITOR_OT_add_transforms,
    SEQUENCE_EDITOR_OT_zoom_transforms,
    SEQUENCE_EDITOR_OT_switch_zooms,
    SEQUENCE_EDITOR_OT_pan_transforms,
    SEQUENCE_EDITOR_OT_crossfade,
    SEQUENCE_EDITOR_OT_slideshow_fade_in_out,
    SEQUENCE_EDITOR_OT_audio_fade_in_out,
    SEQUENCE_EDITOR_OT_pan_start_nw, SEQUENCE_EDITOR_OT_pan_start_n, SEQUENCE_EDITOR_OT_pan_start_ne,
    SEQUENCE_EDITOR_OT_pan_start_w, SEQUENCE_EDITOR_OT_pan_start_0, SEQUENCE_EDITOR_OT_pan_start_e,
    SEQUENCE_EDITOR_OT_pan_start_sw, SEQUENCE_EDITOR_OT_pan_start_s, SEQUENCE_EDITOR_OT_pan_start_se,
    SEQUENCE_EDITOR_OT_pan_end_nw, SEQUENCE_EDITOR_OT_pan_end_n, SEQUENCE_EDITOR_OT_pan_end_ne,
    SEQUENCE_EDITOR_OT_pan_end_w, SEQUENCE_EDITOR_OT_pan_end_0, SEQUENCE_EDITOR_OT_pan_end_e,
    SEQUENCE_EDITOR_OT_pan_end_sw, SEQUENCE_EDITOR_OT_pan_end_s, SEQUENCE_EDITOR_OT_pan_end_se,
    SEQUENCE_EDITOR_OT_pan_random, SEQUENCE_EDITOR_OT_pan_cw, SEQUENCE_EDITOR_OT_pan_ccw,
    SEQUENCE_EDITOR_OT_align_images, SEQUENCE_EDITOR_OT_align_images_center,
    SEQUENCE_EDITOR_OT_align_images_top, SEQUENCE_EDITOR_OT_align_images_bottom,
    SEQUENCE_EDITOR_OT_align_images_left, SEQUENCE_EDITOR_OT_align_images_right,
]


def register():
    for cls in classes: bpy.utils.register_class(cls)  # noqa: E701
    bpy.types.Scene.ddslideshow = bpy.props.PointerProperty(type=DDSlideshowProperties)


def unregister():
    for cls in classes: bpy.utils.unregister_class(cls)  # noqa: E701
    del bpy.types.Scene.ddslideshow


if __name__ == '__main__':
    register()
