import asyncio

import zigpy.types as t
from zigpy.quirks import BatteryCustomDevice, CustomCluster


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


class SmartthingsArrivalCluster(CustomCluster):
    cluster_id = 0xfc05
    name = 'Smartthings Arrival'
    attributes = {}
    server_commands = {
        0x0000: ('beep', (t.uint16_t, ), False),
    }
    client_commands = {
        0x0000: ('battery', (t.uint8_t, ), False),
        0x0001: ('presence', (), False),
    }


class SmartthingsDevice(BatteryCustomDevice):
    _max_voltage = 2800
    _min_voltage = 1500

    def setup_battery_monitoring(self, new_join):
        self.endpoints[1].in_clusters[1].add_listener(self)
        asyncio.ensure_future(self._setup_power_cluster(new_join))

    @asyncio.coroutine
    def _setup_power_cluster(self, new_join):
        if new_join:
            yield from self.endpoints[1].in_clusters[1].bind()
        try:
            yield from self.endpoints[1].in_clusters[1].read_attributes([0x0020])
        except Exception:
            pass

    def attribute_updated(self, attrid, value):
        if attrid == 0x0020:
            self._set_battery(value)

    def _set_battery(self, value):
        battery_percent = round((value * 100 - self._min_voltage) /
                                (self._max_voltage - self._min_voltage) * 100)
        if battery_percent > 100:
            battery_percent = 100
        elif battery_percent < 0:
            battery_percent = 0
        self._battery_voltage = value * 100
        self._battery_percent = battery_percent


class SmartthingsMotionSensor(SmartthingsDevice):
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


class SmartthingsTemperatureHumiditySensor(SmartthingsDevice):
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


class SmartthingsArrivalSensor(SmartthingsDevice):
    signature = [
        {
            # <SimpleDescriptor endpoint=1 profile=260 device_type=410 device_version=0 input_clusters=[0] output_clusters=[]>
            1: {
                'profile_id': 0x0104,
                'device_type': 0x019A,
                'input_clusters': [0],
                'output_clusters': [],
            },
            # <SimpleDescriptor endpoint=2 profile=64513 device_type=410 device_version=0 input_clusters=[] output_clusters=[]>
            2: {
                'profile_id': 0xFC01,
                'device_type': 0x019A,
                'input_clusters': [],
                'output_clusters': [],
            },
        }
    ]

    replacement = {
        'endpoints': {
            2: {
                'input_clusters': [SmartthingsArrivalCluster]
            },
        }
    }

    def setup_battery_monitoring(self, new_join):
        self.endpoints[2].in_clusters[SmartthingsArrivalCluster.cluster_id].add_listener(self)

    def cluster_command(self, tsn, command_id, args):
        if command_id == 0x0000:
            self._set_battery(args[0])

    @asyncio.coroutine
    def beep(self):
        def _beep_sleep():
            def callback(future):
                future.exception()

            cluster = self.endpoints[2].in_clusters[SmartthingsArrivalCluster.cluster_id]
            task = asyncio.ensure_future(cluster.request(
                False,
                0x0000,
                SmartthingsArrivalCluster.server_commands[0x0000][1],
                0x0115,
                manufacturer=0x110A,
                expect_reply=False,
                tries=3,
                delay=2,
            ))
            task.add_done_callback(callback)
            yield from asyncio.sleep(7.0)

        for x in range(5):
            yield from _beep_sleep()
