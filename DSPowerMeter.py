"""This module represent a power meter in a DSBridge
"""

from pyhap.accessory import Accessory
from pyhap.const import CATEGORY_SENSOR

import DSInterface

class DSPowerMeter(Accessory):

    category = CATEGORY_SENSOR

    def __init__(self, driver, interface: DSInterface, *args, **kwargs):
        super().__init__(driver=driver, display_name='power_meter', aid=89237636)

        self._ds_interface = interface
        self._circuit_ids = set()

        serv_power = self.add_preload_service('TemperatureSensor')
        self.char_power = serv_power.configure_char('CurrentTemperature')

        r = self._ds_interface._applycommand('apartment/getCircuits')

        for circuit in r['circuits']:
            if circuit['isPresent'] and circuit['isValid'] and circuit['hasMetering']:
                self._circuit_ids.add(circuit['dsid'])

        print(r)

    @Accessory.run_at_interval(10)
    def run(self):

        sum = 0
        for id in self._circuit_ids:
            r = self._ds_interface._applycommand('circuit/getConsumption', {'id': id})

            sum += r['consumption']

        self.char_power.set_value(sum)
