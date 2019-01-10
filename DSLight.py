"""This module represent a light in a DSBridge
"""

from pyhap.accessory import Accessory
from pyhap.const import CATEGORY_LIGHTBULB

import DSInterface

class DSLight(Accessory):

    category = CATEGORY_LIGHTBULB

    def __init__(self, driver, interface: DSInterface, description: dict, *args, **kwargs):

        self._ds = interface
        self._id = description['id']

        super().__init__(driver=driver, display_name=description['name'], aid=abs(hash(self._id)))

        serv_light = self.add_preload_service('Lightbulb', chars=['On', 'Brightness'])

        self.char_on = serv_light.configure_char(
            'On', setter_callback=self.set_state)
        self.char_on = serv_light.configure_char(
            'Brightness', setter_callback=self.set_brightness)

        self.accessory_state = 0    # State of the neo light On/Off
        self.brightness = 100       # Brightness value 0 - 100 Homekit API


    def set_state(self, value):
#        print("set_state" + value)
        self.accessory_state = value
        if value:
            self.set_brightness(100)
        else:
            self.set_brightness(0)


    def set_brightness(self, value):
#        print("set_brightness" + value)
        self.brightness = value
        self._ds.set_value(self._id, value)

    _ds = 0
    _id = ''

