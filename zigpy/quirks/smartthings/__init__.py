import asyncio

import zigpy.types as t
from zigpy.device import Device
from zigpy.quirks import CustomDevice, CustomCluster


class SmartthingsRelativeHumidityCluster(CustomCluster):
    cluster_id = 0xfc45
    name = 'Smartthings Relative Humidity Measurement'
    ep_attribute = 'humidity'
    attributes = {
        # Relative Humidity Measurement Information
        0x0000: ('measured_value', t.int16s),
    }
    server_commands = {}
    client_commands = {}


class SmartthingsDevice(Device):
    def setup_battery_monitoring(self):
        self._battery_percent = "unknown"
        self._battery_voltage = "unknown"
        self.endpoints[1].in_clusters[1].add_listener(self)
        loop = asyncio.get_event_loop()
        loop.call_soon(asyncio.async, self.setup_power_cluster())

    @asyncio.coroutine
    def setup_power_cluster(self):
        yield from self.endpoints[1].in_clusters[1].bind()
        yield from self.endpoints[1].in_clusters[1].read_attributes([0x0020])

    def attribute_updated(self, attrid, value):
        if attrid == 0x0020:
            battery_percent = round((value * 100 - 1500) /
                                    (2800 - 1500) * 100)
            if battery_percent > 100:
                battery_percent = 100
            elif battery_percent < 0:
                battery_percent = 0
            self._battery_voltage = value * 100
            self._battery_percent = battery_percent

    def cluster_command(self, *args, **kwargs):
        pass

    def zdo_command(self, *args, **kwargs):
        pass

    @property
    def battery_percent(self):
        return self._battery_percent

    @property
    def battery_voltage(self):
        return self._battery_voltage


class SmartthingsMotionSensor(CustomDevice, SmartthingsDevice):
    signature = [
        {
            # <SimpleDescriptor endpoint=1 profile=260 device_type=1026 device_version=0 input_clusters=[0, 1, 3, 1026, 1280, 32, 2821] output_clusters=[25]>
            1: {
                'profile_id': 0x0104,
                'device_type': 0x0402,
                'input_clusters': [0, 1, 3, 1026, 1280, 32, 2821],
                'output_clusters': [25],
            },
            # <SimpleDescriptor endpoint=2 profile=49887 device_type=263 device_version=0 input_clusters=[0, 1, 3, 2821, 64582] output_clusters=[3]>
            2: {
                'profile_id': 0xC2DF,
                'device_type': 0x0107,
                'input_clusters': [0, 1, 3, 2821, 64582],
                'output_clusters': [3],
            }
        }
    ]

    replacement = {
        'endpoints': {
            1: {
                'input_clusters': [0x0000, 0x0001, 0x0003, 0x0402, 0x0500,
                                   0x0020, 0x0B05],
            }
        }
    }


class SmartthingsTemperatureHumiditySensor(CustomDevice, SmartthingsDevice):
    signature = [
        {
            # <SimpleDescriptor endpoint=1 profile=260 device_type=770 device_version=0 input_clusters=[0, 1, 3, 32, 1026, 2821, 64581] output_clusters=[3, 25]>
            1: {
                'profile_id': 0x0104,
                'device_type': 0x0302,
                'input_clusters': [0, 1, 3, 32, 1026, 2821, 64581],
                'output_clusters': [3, 25],
            }
        }
    ]

    replacement = {
        'endpoints': {
            1: {
                'input_clusters': [0x0000, 0x0001, 0x0003, 0x0402, 0x0B05,
                                   SmartthingsRelativeHumidityCluster],
            }
        }
    }
