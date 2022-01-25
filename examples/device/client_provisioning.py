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
from vl_device_mqtt import VLDeviceMqttClient, VLPublishInfo
logging.basicConfig(level=logging.DEBUG)


def main():
    """
    We can provide the following parameters to provisioning function:
      host - required - Host of ViraLink
      provision_device_key - required - device provision key from device profile
      provision_device_secret - required - device provision secret from device profile
      port=1883 - not required - MQTT port of ViraLink instance
      device_name=None - may be generated on ViraLink - You may pass here name for device, if this parameter is not assigned, the name will be generated

      ### Credentials type = ACCESS_TOKEN

      access_token=None - may be generated on ViraLink - You may pass here some access token and it will be saved as accessToken for device on ViraLink.

      ### Credentials type = MQTT_BASIC

      client_id=None - not required (if username is not None) - You may pass here client Id for your device and use it later for connecting
      username=None - not required (if client id is not None) - You may pass here username for your client and use it later for connecting
      password=None - not required - You may pass here password and use it later for connecting

      ### Credentials type = X509_CERTIFICATE
      hash=None - required (If you wanna use this credentials type) - You should pass here public key of the device, generated from mqttserver.jks

    """

    # Call device provisioning, to do this we don't need an instance of the VLDeviceMqttClient to provision device

    credentials = VLDeviceMqttClient.provision("console.viralink.io", "PROVISION_DEVICE_KEY", "PROVISION_DEVICE_SECRET")

    if credentials is not None:
        client = VLDeviceMqttClient("console.viralink.io", credentials)
        client.connect()
        # Sending data in async way

        client.stop()


if __name__ == '__main__':
    main()
