#coding: utf-8

#author: Aderbal Machado Ribeiro

import os, PIL, zbarlight

from collections import namedtuple
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.utils import platform

try:
    # Pillow
    PIL.Image.frombytes
    PIL.Image.Image.tobytes
except AttributeError:
    # PIL
    PIL.Image.frombytes = PIL.Image.frombuffer
    PIL.Image.Image.tobytes = PIL.Image.Image.tostring

MODULE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
Builder.load_file(os.path.join(MODULE_DIRECTORY, "zbarcam.kv"))


class ZBarCam(AnchorLayout):
    """
    Widget that use the Camera and zbar to detect qrcode.
    When found, the `symbols` will be updated.
    """
    resolution = ListProperty([640, 480])

    symbols = ListProperty([])
    Symbol = namedtuple('Symbol', ['type', 'data'])
    code_types = ListProperty(zbarlight.Symbologies.keys())

    def __init__(self, **kwargs):
        super(ZBarCam, self).__init__(**kwargs)
        Clock.schedule_once(lambda dt: self._setup())

    def _setup(self):
        self._remove_shoot_button()
        self._enable_android_autofocus()
        self.xcamera._camera.bind(on_texture=self._on_texture)

    def _remove_shoot_button(self):
        xcamera = self.xcamera
        shoot_button = xcamera.children[0]
        xcamera.remove_widget(shoot_button)

    def _enable_android_autofocus(self):
        if not self.is_android(): return
        camera = self.xcamera._camera._android_camera
        params = camera.getParameters()
        params.setFocusMode('continuous-video')
        camera.setParameters(params)

    def _on_texture(self, instance):
        self._detect_qrcode_frame(instance=None, camera=instance, texture=instance.texture)

    def _detect_qrcode_frame(self, instance, camera, texture):
        image_data = texture.pixels
        size = texture.size
        fmt = texture.colorfmt.upper()
        pil_image = PIL.Image.frombytes(mode=fmt, size=size, data=image_data)
        symbols = []
        for code_type in self.code_types:
            codes = zbarlight.scan_codes(code_type, pil_image) or []
            for code in codes:
                symbol = ZBarCam.Symbol(type=code_type, data=code)
                symbols.append(symbol)
        self.symbols = symbols

    @property
    def xcamera(self):
        return self.ids['xcamera']

    def start(self):
        self.xcamera.play = True

    def stop(self):
        self.xcamera.play = False

    def is_android(self):
        return platform == 'android'
