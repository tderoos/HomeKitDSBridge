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


class DSBridge(Bridge):
    """DSBridge exposes a DigitalStrom setup"""

    category = CATEGORY_OTHER

    def __init__(self, driver, address, app_token, *args, **kwargs):

        super().__init__(driver, 'DSBridge', *args, **kwargs)

        interface = DSInterface()
        interface.connect(address, app_token)

        self._init_config(interface)

    def _init_config(self, interface: DSInterface):

        zones = interface.get_zones()

        for zone in zones:
            # Zone with ID 0 is a special zone that contains all devices.
            if zone != 0:# and zone == 5:
                self._init_zone(interface, zone)

#        r = interface.get_devices_for_zone('slaapkamer 1')

 #       light = DSLight(self.driver, interface, r[0])
  #      self.add_accessory(light)


    def _init_zone(self, interface: DSInterface, zone):
        devices = interface.get_devices_for_zone(zone)

        for device in devices:
            self._init_device(interface, device)


    def _init_device(self, interface: DSInterface, device:dict):
        if device['functionID'] == 4369 and device['outputMode'] != 0:
            light = DSLight(self.driver, interface, device)
            self.add_accessory(light)
