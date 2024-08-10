import bpy

from .panel import SEQUENCE_EDITOR_PT_workflow, SEQUENCE_EDITOR_PT_settings
from .properties import DDSlideshowProperties
from .operators import (SEQUENCE_EDITOR_OT_create_slideshow,
                        SEQUENCE_EDITOR_OT_load_images,
                        SEQUENCE_EDITOR_OT_overlap_images,
                        SEQUENCE_EDITOR_OT_add_transforms,
                        SEQUENCE_EDITOR_OT_zoom_transforms,
                        SEQUENCE_EDITOR_OT_pan_transforms,
                        SEQUENCE_EDITOR_OT_crossfade,
                        SEQUENCE_EDITOR_OT_slideshow_fade_in_out,
                        SEQUENCE_EDITOR_OT_audio_fade_in_out)


classes = [DDSlideshowProperties,
           SEQUENCE_EDITOR_PT_workflow,
           SEQUENCE_EDITOR_PT_settings,
           SEQUENCE_EDITOR_OT_create_slideshow,
           SEQUENCE_EDITOR_OT_load_images,
           SEQUENCE_EDITOR_OT_overlap_images,
           SEQUENCE_EDITOR_OT_add_transforms,
           SEQUENCE_EDITOR_OT_zoom_transforms,
           SEQUENCE_EDITOR_OT_pan_transforms,
           SEQUENCE_EDITOR_OT_crossfade,
           SEQUENCE_EDITOR_OT_slideshow_fade_in_out,
           SEQUENCE_EDITOR_OT_audio_fade_in_out]


def register():
    for cls in classes: bpy.utils.register_class(cls)  # noqa: E701
    bpy.types.Scene.ddslideshow = bpy.props.PointerProperty(type=DDSlideshowProperties)



def unregister():
    for cls in classes: bpy.utils.unregister_class(cls)  # noqa: E701
    del bpy.types.Scene.ddslideshow


if __name__ == '__main__':
    register()

