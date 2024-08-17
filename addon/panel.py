from bpy.types import Panel


class SEQUENCE_EDITOR_PT_run_workflow(Panel):
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'DDSlideshow'
    bl_label = 'Workflow'

    def draw(self, context):
        layout = self.layout

        layout.operator('ddslideshow.run_workflow', text='Run all')

        layout.separator()

        layout.operator('ddslideshow.load_images', text='Load images')
        layout.operator('ddslideshow.overlap_images', text='Overlap images')
        layout.operator('ddslideshow.add_transforms', text='Add transforms')
        layout.operator('ddslideshow.zoom_transforms', text='Apply zoom')
        layout.operator('ddslideshow.pan_transforms', text='Apply pan')
        layout.operator('ddslideshow.crossfade', text='Add crossfade')
        layout.operator('ddslideshow.slideshow_fade_in_out', text='Slideshow fade in/out')
        layout.operator('ddslideshow.audio_fade_in_out', text='Audio fade in/out')


class SEQUENCE_EDITOR_PT_media(Panel):
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'DDSlideshow'
    bl_label = 'Media Settings'

    def draw(self, context):
        scene = context.scene
        ddslideshow = scene.ddslideshow

        layout = self.layout

        layout.prop(ddslideshow, 'intro')
        layout.prop(ddslideshow, 'outro')
        layout.prop(ddslideshow, 'audio')

        layout.separator()
        layout.label(text='Scale and alignment:')
        layout.prop(ddslideshow, 'scale_method', text='Scale method')

        layout.prop(ddslideshow, 'align_x', text='Horizontal align')
        layout.prop(ddslideshow, 'align_y', text='Vertical align')
        layout.operator('ddslideshow.load_images')


class SEQUENCE_EDITOR_PT_per_slide(Panel):
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'DDSlideshow'
    bl_label = 'Per Slide Settings'

    def draw(self, context):
        scene = context.scene
        ddslideshow = scene.ddslideshow

        layout = self.layout

        row = layout.row()
        row.prop(ddslideshow, 'slide_duration')
        row.prop(ddslideshow, 'slide_crossfade')

        layout.operator('ddslideshow.overlap_images', text='Overlap images')
        layout.operator('ddslideshow.add_transforms', text='Add transforms')


class SEQUENCE_EDITOR_PT_zoom_pan_settings(Panel):
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'DDSlideshow'
    bl_label = 'Zoom/Pan settings'

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
        layout.operator('ddslideshow.switch_zooms')

        layout.separator()

        layout.label(text='Pan:')

        layout.prop(ddslideshow, 'zoom_center_downscaled')

        split = layout.split()
        left = split.column().box()
        right = split.column().box()

        left.label(text='From:')

        grid = left.grid_flow(columns=3, row_major=True)
        grid.operator('ddslideshow.pan_start_nw', text='NW')
        grid.operator('ddslideshow.pan_start_n')
        grid.operator('ddslideshow.pan_start_ne')
        grid.operator('ddslideshow.pan_start_w')
        grid.operator('ddslideshow.pan_start_0')
        grid.operator('ddslideshow.pan_start_e')
        grid.operator('ddslideshow.pan_start_sw')
        grid.operator('ddslideshow.pan_start_s')
        grid.operator('ddslideshow.pan_start_se')

        right.label(text='To:')

        grid = right.grid_flow(columns=3, row_major=True)
        grid.operator('ddslideshow.pan_end_nw')
        grid.operator('ddslideshow.pan_end_n')
        grid.operator('ddslideshow.pan_end_ne')
        grid.operator('ddslideshow.pan_end_w')
        grid.operator('ddslideshow.pan_end_0')
        grid.operator('ddslideshow.pan_end_e')
        grid.operator('ddslideshow.pan_end_sw')
        grid.operator('ddslideshow.pan_end_s')
        grid.operator('ddslideshow.pan_end_se')

        layout.operator('ddslideshow.pan_random')
        layout.operator('ddslideshow.pan_cw')
        layout.operator('ddslideshow.pan_ccw')


class SEQUENCE_EDITOR_PT_transitions(Panel):
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'DDSlideshow'
    bl_label = 'Transitions'

    def draw(self, context):
        layout = self.layout

        layout.operator('ddslideshow.crossfade', text='Add crossfade')
        layout.operator('ddslideshow.slideshow_fade_in_out', text='Slideshow fade in/out')
        layout.operator('ddslideshow.audio_fade_in_out', text='Audio fade in/out')
