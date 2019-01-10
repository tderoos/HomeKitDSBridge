"""This module provides DSBridge - an bridge that exposes a
DigitalStrom setup.
"""

from pyhap.accessory import Bridge
from pyhap.const import CATEGORY_OTHER

from urllib.parse import urlencode
import requests
import json

from DigitalStrom import DigitalStrom
from DSLight import DSLight


class DSBridge(Bridge):
    """DSBridge exposes a DigitalStrom setup"""

    category = CATEGORY_OTHER

    def __init__(self, driver, address, app_token, *args, **kwargs):

        super().__init__(driver, 'DSBridge', *args, **kwargs)

        self._DSInterface = DigitalStrom()
        self._DSInterface.connect(address, app_token)

        self._init_config()

    def apply_command(self, command, parameters={}) -> bool:
        if self._session_token != "":
            parameters["token"] = self._session_token

        url = self._base_url + command + '?' + urlencode(parameters)

        r = requests.get(url, verify=False)
        return json.loads(r.text).get("result", {})


    def _init_config(self):
        r = self._DSInterface.getDevicesForZone('slaapkamer 1')

        light = DSLight(self, r[0])
        self.add_accessory(light)



    _DSInterface = ""
    _session_token = ""
