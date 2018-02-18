from zigpy.quirks import CustomDevice

class TemperatureHumiditySensor(CustomDevice):
    signature = {
        # <SimpleDescriptor endpoint=1 profile=260 device_type=24321 device_version=1 input_clusters=[0, 3, 25, 65535, 18] output_clusters=[0, 4, 3, 5, 25, 65535, 18]>
        1: {
            'profile_id': 0x0104,
            'device_type': 0x5f01,
            'input_clusters': [0, 3, 25, 65535, 18],
            'output_clusters': [0, 4, 3, 5, 25, 65535, 18],
        },
        # <SimpleDescriptor endpoint=2 profile=260 device_type=24322 device_version=1 input_clusters=[3, 18] output_clusters=[4, 3, 5, 18]>
        2: {
            'profile_id': 0x0104,
            'device_type': 0x5f02,
            'input_clusters': [3, 18],
            'output_clusters': [4, 3, 5, 18],
        },
        # <SimpleDescriptor endpoint=3 profile=260 device_type=24323 device_version=1 input_clusters=[3, 12] output_clusters=[4, 3, 5, 12]>
        3: {
            'profile_id': 0x0104,
            'device_type': 0x5f03,
            'input_clusters': [3, 12],
            'output_clusters': [4, 3, 5, 12],
        },
    }

    replacement = {
        'endpoints': {
            1: {
                'input_clusters': [0x0000, 0x0003, 0x0402, 0x0405],
            }
        },
    }
