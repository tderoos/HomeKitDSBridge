from urllib.parse import urlencode
import requests
import json
from requests.auth import HTTPBasicAuth

# Requests are currently not secure
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class DSInterface:

    def __init__(self):
        print("connecting")


    def connect(self, url, app_token):
        self._base_url = url + "/json/"
        r = self._applycommand("system/loginApplication", {"loginToken": app_token})
        self._session_token = r["token"]

        r = self._applycommand("apartment/getStructure")
        self._zones = r['apartment']['zones']


    def get_zones(self):
        zones = {}

        for zone in self._zones:
            if zone["isPresent"]:
                zones[zone['id']] = zone["name"]

        return zones

    def get_devices_for_zone(self, zone_id):

        for zone in self._zones:
            if zone['id'] == zone_id or zone['name'] == zone_id:
                return zone['devices']
        # for zone in self._zones:
        #     if zone['id'] == zone_id or zone['name'] == zone_id:
        #         devices = list()
        #
        #         for device in zone['devices']:
        #             devices.append({'name': device['name'], 'id': device['id']})
        #         return devices

        return None

    def set_value(self, device_id, value):
        self._applycommand('device/setValue', {'dsid': device_id, 'value': value})

    def get_values(self, device_id):
        return self._applycommand2('device/getOutputValue', {'dsid': device_id})

    def _applycommand(self, command, parameters={}):
#        assert(self._session_token != "")

        if self._session_token != "":
            parameters["token"] = self._session_token

        url = self._base_url + command + '?' + urlencode(parameters)

        print(url)

        r = requests.get(url, verify=False)
        return json.loads(r.text).get("result", {})


    def _applycommand2(self, command, parameters={}):
        #        assert(self._session_token != "")

        if self._session_token != "":
            parameters["token"] = self._session_token

        url = self._base_url + command + '?' + urlencode(parameters)

        print(url)

        r = requests.get(url, verify=False)
        return json.loads(r.text)

    _base_url = ""
    _session_token = ""
    _zones = {}
