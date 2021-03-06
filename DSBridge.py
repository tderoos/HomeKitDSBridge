"""This module provides DSBridge - an bridge that exposes a
DigitalStrom setup.
"""

from pyhap.accessory import Bridge
from pyhap.const import CATEGORY_OTHER

from urllib.parse import urlencode
import requests
import json

from DSInterface import DSInterface
from DSLight import DSLight
from DSPowerMeter import DSPowerMeter


class DSBridge(Bridge):
    """DSBridge exposes a DigitalStrom setup"""

    category = CATEGORY_OTHER

    def __init__(self, driver, address, app_token, *args, **kwargs):

        super().__init__(driver, 'DSBridge', *args, **kwargs)

        interface = DSInterface()
        interface.connect(address, app_token)

        self._init_config(interface)

    def _init_config(self, interface: DSInterface):

        power_meter = DSPowerMeter(self.driver, interface)
        self.add_accessory(power_meter)

        for zone in interface.get_zones():
            # Zone with ID 0 is a special zone that contains all devices.
            if zone != 0:# and zone == 5:
                self._init_zone(interface, zone)

    def _init_zone(self, interface: DSInterface, zone):
        devices = interface.get_devices_for_zone(zone)

        for device in devices:
            self._init_device(interface, device)


    def _init_device(self, interface: DSInterface, device:dict):
        if device['functionID'] == 4369 and device['outputMode'] != 0:
            light = DSLight(self.driver, interface, device)
            self.add_accessory(light)
