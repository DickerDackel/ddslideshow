from bpy.types import Panel


class SEQUENCE_EDITOR_PT_settings_ng(Panel):
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'DDSlideshow'
    bl_label = 'Settings Ng'

    def draw(self, context):
        scene = context.scene
        ddslideshow = scene.ddslideshow

        layout = self.layout

        layout.label(text='Zoom:')

        split = layout.split()
        left = split.column()
        right = split.column()

        left.prop(ddslideshow, 'zoom_from')
        right.prop(ddslideshow, 'zoom_to')
        layout.prop(ddslideshow, 'zoom_randomize')
        layout.operator('ddslideshow.zoom_transforms')

        layout.separator()
        layout.label(text='Pan:')

        split = layout.split()
        left = split.column().box()
        right = split.column().box()

        left.label(text='From:')
        right.label(text='To:')

        lsplit = left.split()
        col = lsplit.column()
        grid = col.grid_flow(columns=3)
        grid.operator('ddslideshow.pan_start_nw')
        grid.operator('ddslideshow.pan_start_n')
        grid.operator('ddslideshow.pan_start_ne')
        grid.operator('ddslideshow.pan_start_w')
        grid.operator('ddslideshow.pan_start_0')
        grid.operator('ddslideshow.pan_start_e')
        grid.operator('ddslideshow.pan_start_sw')
        grid.operator('ddslideshow.pan_start_s')
        grid.operator('ddslideshow.pan_start_se')

        col = lsplit.column()
        col.operator('ddslideshow.pan_start_random')
        col.operator('ddslideshow.pan_start_cw')
        col.operator('ddslideshow.pan_start_ccw')


        rsplit = right.split()
        col = rsplit.column()
        grid = col.grid_flow(columns=3)
        grid.operator('ddslideshow.pan_end_nw')
        grid.operator('ddslideshow.pan_end_n')
        grid.operator('ddslideshow.pan_end_ne')
        grid.operator('ddslideshow.pan_end_w')
        grid.operator('ddslideshow.pan_end_0')
        grid.operator('ddslideshow.pan_end_e')
        grid.operator('ddslideshow.pan_end_sw')
        grid.operator('ddslideshow.pan_end_s')
        grid.operator('ddslideshow.pan_end_se')

        col = rsplit.column()
        col.operator('ddslideshow.pan_end_random')
        col.operator('ddslideshow.pan_end_cw')
        col.operator('ddslideshow.pan_end_ccw')


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

        col = layout.column()
        row = col.row()
        row.prop(ddslideshow, 'zoom_randomize')

        col = layout.column()
        row = col.row()
        row.prop(ddslideshow, 'pan')
