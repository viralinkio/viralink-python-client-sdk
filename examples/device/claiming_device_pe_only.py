#      Copyright 2020. ViraLink
#  #
#      Licensed under the Apache License, Version 2.0 (the "License");
#      you may not use this file except in compliance with the License.
#      You may obtain a copy of the License at
#  #
#          http://www.apache.org/licenses/LICENSE-2.0
#  #
#      Unless required by applicable law or agreed to in writing, software
#      distributed under the License is distributed on an "AS IS" BASIS,
#      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#      See the License for the specific language governing permissions and
#      limitations under the License.
#

import logging
import time

from vl_device_mqtt import VLDeviceMqttClient
logging.basicConfig(level=logging.DEBUG)

VIRALINK_HOST = "console.viralink.io"
DEVICE_ACCESS_TOKEN = "DEVICE_ACCESS_TOKEN"

SECRET_KEY = "DEVICE_SECRET_KEY"  # Customer should write this key in device claiming widget
DURATION = 30000  # In milliseconds (30 seconds)


def main():
    client = VLDeviceMqttClient(VIRALINK_HOST, DEVICE_ACCESS_TOKEN)
    client.connect()
    rc = client.claim(secret_key=SECRET_KEY, duration=DURATION).get()
    if rc == 0:
        print("Claiming request was sent.")
    client.stop()


if __name__ == '__main__':
    main()
