"""This module represent a light in a DSBridge
"""

from pyhap.accessory import Accessory
from pyhap.const import CATEGORY_LIGHTBULB

import DSInterface

dimmed = 22
switched = 16


class DSLight(Accessory):

    category = CATEGORY_LIGHTBULB

    def __init__(self, driver, interface: DSInterface, description: dict, *args, **kwargs):

        self._ds = interface
        self._id = description['id']

        super().__init__(driver=driver, display_name=description['name'], aid=abs(hash(self._id)))

        print(description['name'])

        chars = ['On']
        if description['outputMode'] == 22:
            chars.append('Brightness')

        serv_light = self.add_preload_service('Lightbulb', chars=chars)

        # Get the current value for the device
        r = interface._applycommand('device/getConfig', {'dsid': self._id, 'class':64, 'index':0})
        value = r['value']

        self.char_on = serv_light.configure_char(
            'On', setter_callback=self.set_state)
        self.char_on.set_value(1 if value != 0 else 0)   # State of the neo light On/Off

        if description['outputMode'] == 22:
            self.char_brightness = serv_light.configure_char(
                'Brightness', setter_callback=self.set_brightness)

            self.brightness = int(value * 100 / 255)
            self.char_brightness.set_value(self.brightness, should_notify=False)
        else:
            self.brightness = 100


#        r = interface.get_values(self._id)


    def set_state(self, value):
        if value:
            self.set_brightness(self.brightness)
        else:
            self._ds.set_value(self._id, 0)


    def set_brightness(self, value):
        self.brightness = value

        value = int((value * 255) / 100)
        self._ds.set_value(self._id, value)

    _ds = 0
    _id = ''

