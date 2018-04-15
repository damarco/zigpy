from zigpy.quirks import CustomDevice, CustomEndpoint
from zigpy.profiles import zha


class HueColorBulb(CustomDevice):
    class HueEndpoint(CustomEndpoint):
        # Hue bulb expects HA profile id in messages
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

    signature = [
        {
            # <SimpleDescriptor endpoint=242 profile=41440 device_type=97 device_version=0 input_clusters=[33] output_clusters=[33]>
            242: {
                'profile_id': 0xa1e0,
                'device_type': 0x0061,
                'input_clusters': [33],
                'output_clusters': [33],
            },
            #  <SimpleDescriptor endpoint=11 profile=49246 device_type=528 device_version=2 input_clusters=[0, 3, 4, 5, 6, 8, 768, 4096, 64513] output_clusters=[25]>
            11: {
                'profile_id': 0xc05e,
                'device_type': 0x0210,
                'input_clusters': [0, 3, 4, 5, 6, 8, 768, 4096, 64513],
                'output_clusters': [25],
            }
        }
    ]

    replacement = {
        'endpoints': {
            11: (HueEndpoint, {
                'input_clusters': [0, 3, 4, 5, 6, 8, 768, 4096, 64513],
                'output_clusters': [25],
            })
        }
    }
