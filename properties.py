import bpy

from bpy.props import BoolProperty, EnumProperty, FloatProperty


class DDSlideshowProperties(bpy.types.PropertyGroup):
    intro: bpy.props.StringProperty(name='Intro Slide', subtype='FILE_PATH', default='')
    outro: bpy.props.StringProperty(name='Outro Slide', subtype='FILE_PATH', default='')
    audio: bpy.props.StringProperty(name='Audio Track', subtype='FILE_PATH', default='')

    slide_duration: FloatProperty(subtype='TIME', name='duration', default=5, min=0.0001, soft_min=1, soft_max=10)
    slide_crossfade: FloatProperty(subtype='TIME', name='crossfade', default=3, min=0, soft_min=1, soft_max=5)

    zoom_from: FloatProperty(name='Zoom from', default=1, min=0, soft_max=2)
    zoom_to: FloatProperty(name='Zoom to', default=1.5, min=0, soft_max=2)
    zoom_randomize: BoolProperty(name='Randomize zoom direction', default=True)

    pan: EnumProperty(name='Pan',
                      default='randomize',
                      items=[('off', 'Off', ''),
                             ('randomize', 'Randomize', ''),
                             ('cw', 'Clockwise', ''), ('ccw', 'Counter clockwise', ''),
                             ('nw', 'NW', ''), ('n', 'N', ''), ('ne', 'NE', ''),
                             ('w', 'W', ''), ('e', 'E', ''),
                             ('sw', 'SW', ''), ('s', 'S', ''), ('se', 'SE', '')])

    slideshow_fade_in: FloatProperty(subtype='TIME', name='Fade in', default=5, min=0, soft_max=10)
    slideshow_fade_out: FloatProperty(subtype='TIME', name='Fade out', default=5, min=0, soft_max=10)

    audio_fade_in: FloatProperty(subtype='TIME', name='Fade in', default=5, min=0, soft_max=10)
    audio_fade_out: FloatProperty(subtype='TIME', name='Fade out', default=5, min=0, soft_max=10)
