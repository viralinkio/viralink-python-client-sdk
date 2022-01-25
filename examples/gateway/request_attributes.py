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

from vl_gateway_mqtt import VLGatewayMqttClient
logging.basicConfig(level=logging.DEBUG)


def callback(client, result, exception):
    client.stop()
    if exception is not None:
        print("Exception: " + str(exception))
    else:
        print(result)


def main():
    gateway = VLGatewayMqttClient("console.viralink.io", "TEST_GATEWAY_TOKEN")
    gateway.connect()
    gateway.gw_request_shared_attributes("Example Name", ["temperature"], callback)

    while not gateway.stopped:
        time.sleep(1)


if __name__ == '__main__':
    main()
