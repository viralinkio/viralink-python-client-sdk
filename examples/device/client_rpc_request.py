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

import time
import logging
from vl_device_mqtt import VLDeviceMqttClient
logging.basicConfig(level=logging.DEBUG)


def callback(client, request_id, resp_body, exception):
    client.stop()
    if exception is not None:
        print("Exception: " + str(exception))
    else:
        print("request id: {request_id}, response body: {resp_body}".format(request_id=request_id,
                                                                            resp_body=resp_body))


def main():
    client = VLDeviceMqttClient("console.viralink.io", "A2_TEST_TOKEN")

    client.connect()
    # call "getTime" on server and receive result, then process it with callback
    client.send_rpc_call("getTime", {}, callback)
    while not client.stopped:
        time.sleep(1)


if __name__ == '__main__':
    main()
