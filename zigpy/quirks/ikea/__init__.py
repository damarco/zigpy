from zigpy.quirks import CustomDevice, CustomEndpoint
from zigpy.profiles import zha


class TradfriEndpoint(CustomEndpoint):
    # Tradfri bulb expects HA profile id in messages
    def request(self, cluster, sequence, data, expect_reply=True):
        return self.device.request(
            zha.PROFILE_ID,
            cluster,
            self._endpoint_id,
            self._endpoint_id,
            sequence,
            data,
            expect_reply=expect_reply
        )

    def reply(self, cluster, sequence, data):
        return self.device.reply(
            zha.PROFILE_ID,
            cluster,
            self._endpoint_id,
            self._endpoint_id,
            sequence,
            data,
        )


class TradfriTuneableWhiteBulb(CustomDevice):
    signature = [
        {
            # <SimpleDescriptor endpoint=1 profile=49246 device_type=544 device_version=2 input_clusters=[0, 3, 4, 5, 6, 8, 768, 2821, 4096] output_clusters=[5, 25, 32, 4096]>
            1: {
                'profile_id': 0xc05e,
                'device_type': 0x0220,
                'input_clusters': [0, 3, 4, 5, 6, 8, 768, 2821, 4096],
                'output_clusters': [5, 25, 32, 4096],
            },
        }
    ]

    replacement = {
        'endpoints': {
            1: (TradfriEndpoint, {
                'input_clusters': [0, 3, 4, 5, 6, 8, 768, 2821, 4096],
                'output_clusters': [5, 25, 32, 4096],
            })
        }
    }


class TradfriColorBulb(CustomDevice):
    signature = [
        {
            # <SimpleDescriptor endpoint=1 profile=49246 device_type=512 device_version=2 input_clusters=[0, 3, 4, 5, 6, 8, 768, 2821, 4096] output_clusters=[5, 25, 32, 4096]>
            1: {
                'profile_id': 0xc05e,
                'device_type': 0x0200,
                'input_clusters': [0, 3, 4, 5, 6, 8, 768, 2821, 4096],
                'output_clusters': [5, 25, 32, 4096],
            },
        }
    ]

    replacement = {
        'endpoints': {
            1: (TradfriEndpoint, {
                'input_clusters': [0, 3, 4, 5, 6, 8, 768, 2821, 4096],
                'output_clusters': [5, 25, 32, 4096],
            })
        }
    }