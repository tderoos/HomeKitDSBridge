"""This module represent a light in a DSBridge
"""

from pyhap.accessory import Accessory
from pyhap.const import CATEGORY_LIGHTBULB

import DSBridge

class DSLight(Accessory):

    category = CATEGORY_LIGHTBULB

    def __init__(self, bridge: DSBridge, description: dict, *args, **kwargs):
        super().__init__(driver=bridge.driver, display_name=description['name'], aid=1254514)
        self._bridge = bridge

        serv_light = self.add_preload_service('Lightbulb', chars=['On', 'Brightness'])

        self.char_on = serv_light.configure_char(
            'On', setter_callback=self.set_state)
        self.char_on = serv_light.configure_char(
            'Brightness', setter_callback=self.set_brightness)

        self.accessory_state = 0    # State of the neo light On/Off
        self.brightness = 100       # Brightness value 0 - 100 Homekit API


    def set_state(self, value):
        self.accessory_state = value
        if value:
            self.set_brightness(100)
        else:
            self.set_brightness(0)


    def set_brightness(self, value):
        self.brightness = value
        self.set_hue(self.hue)

        _bridge.apply_command("")


    _bridge = 0

