from bpy.types import Panel

class SEQUENCE_EDITOR_PT_workflow(Panel):
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'DDSlideshow'
    bl_label = 'Workflow'

    def draw(self, context):
        layout = self.layout

        layout.operator('ddslideshow.create_slideshow', text='Run all')

        layout.separator()

        layout.operator('ddslideshow.load_images', text='Load images')
        layout.operator('ddslideshow.overlap_images', text='Overlap images')
        layout.operator('ddslideshow.add_transforms', text='Add transforms')
        layout.operator('ddslideshow.zoom_transforms', text='Apply zoom')
        layout.operator('ddslideshow.pan_transforms', text='Apply pan')
        layout.operator('ddslideshow.crossfade', text='Add crossfade')
        layout.operator('ddslideshow.slideshow_fade_in_out', text='Slideshow fade in/out')
        layout.operator('ddslideshow.audio_fade_in_out', text='Audio fade in/out')


class SEQUENCE_EDITOR_PT_settings(Panel):
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'DDSlideshow'
    bl_label = 'Settings'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        ddslideshow = scene.ddslideshow

        layout.operator('ddslideshow.create_slideshow', text='Generate')

        layout.label(text='Media')

        layout.prop(ddslideshow, 'intro')
        layout.prop(ddslideshow, 'outro')
        layout.prop(ddslideshow, 'audio')

        layout.separator()
        layout.label(text='Global settings')

        col = layout.column()
        row = col.row(heading='Slideshow:')
        row.prop(ddslideshow, 'slideshow_fade_in')
        row.prop(ddslideshow, 'slideshow_fade_out')

        col = layout.column()
        row = col.row(heading='Audio:')
        row.prop(ddslideshow, 'audio_fade_in')
        row.prop(ddslideshow, 'audio_fade_out')

        layout.separator()
        layout.label(text='Per slide settings')

        col = layout.column()
        row = col.row()
        row.prop(ddslideshow, 'slide_duration')
        row.prop(ddslideshow, 'slide_crossfade')

        col = layout.column()
        row = col.row()
        row.prop(ddslideshow, 'zoom_from')
        row.prop(ddslideshow, 'zoom_to')
        row.prop(ddslideshow, 'zoom_random')

        col = layout.column()
        row = col.row()
        row.prop(ddslideshow, 'zoom_random')

        col = layout.column()
        row = col.row()
        row.prop(ddslideshow, 'pan')
