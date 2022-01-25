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

from vl_device_mqtt import VLDeviceMqttClient
logging.basicConfig(level=logging.DEBUG)


def callback(client, result):
    print(client, result)


def main():
    client = VLDeviceMqttClient("console.viralink.io", "A2_TEST_TOKEN")
    client.connect()
    sub_id_1 = client.subscribe_to_attribute("uploadFrequency", callback)
    sub_id_2 = client.subscribe_to_all_attributes(callback)
    client.unsubscribe_from_attribute(sub_id_1)
    client.unsubscribe_from_attribute(sub_id_2)


if __name__ == '__main__':
    main()
