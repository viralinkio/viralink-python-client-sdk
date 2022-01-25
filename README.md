# ViraLink MQTT and HTTP client Python SDK

[//]: # (<a href="https://viralink.io"><img src="./logo.png?raw=true" width="100" height="100"></a>)

ViraLink is an IoT platform for data collection, processing, visualization, and device management.
This project ia a Python library that provides convenient client SDK for both Device and [Gateway](https://blog.viralink.io/docs/client-side/mqtt-gateway-api/) APIs.

This repository is the fork of [thingsboard-python-sdk](https://github.com/thingsboard/thingsboard-python-client-sdk)

SDK supports:
- Unencrypted and encrypted (TLS v1.2) connection
- QoS 0 and 1 (MQTT only)
- Automatic reconnect
- All [Device MQTT](https://blog.viralink.io/docs/client-side/mqtt-api/) APIs provided by ViraLink
- All [Gateway MQTT](https://blog.viralink.io/docs/client-side/mqtt-gateway-api/) APIs provided by ViraLink
- Most [Device HTTP](https://blog.viralink.io/docs/client-side/http-api/) APIs provided by ViraLink
  - Device Claiming and Firmware updates are not supported yet.

The [Device MQTT](https://blog.viralink.io/docs/client-side/mqtt-api/) API and the [Gateway MQTT](https://blog.viralink.io/docs/client-side/mqtt-gateway-api/) API are base on the Paho MQTT library. The [Device HTTP](https://blog.viralink.io/docs/client-side/http-api/) API is based on the Requests library.

## Installation

To install using pip:

```bash
pip3 install vl-mqtt-client
```

## Getting Started

Client initialization and telemetry publishing
### MQTT

```python
from vl_device_mqtt import VLDeviceMqttClient, VLPublishInfo

telemetry = {"temperature": 41.9, "enabled": False, "currentFirmwareVersion": "v1.2.2"}
client = VLDeviceMqttClient("console.viralink.io", "A1_TEST_TOKEN")
# Connect to ViraLink
client.connect()
# Sending telemetry without checking the delivery status
client.send_telemetry(telemetry)
# Sending telemetry and checking the delivery status (QoS = 1 by default)
result = client.send_telemetry(telemetry)
# get is a blocking call that awaits delivery status  
success = result.get() == VLPublishInfo.VL_ERR_SUCCESS
# Disconnect from ViraLink
client.disconnect()
```
`

## Using Device APIs

**VLDeviceMqttClient** provides access to Device MQTT APIs of ViraLink platform. It allows to publish telemetry and attribute updates, subscribe to attribute changes, send and receive RPC commands, etc. Use **VLHTTPClient** for the Device HTTP API.
#### Subscription to attributes
##### MQTT

```python
import time
from vl_device_mqtt import VLDeviceMqttClient


def on_attributes_change(client, result, exception):
  if exception is not None:
    print("Exception: " + str(exception))
  else:
    print(result)


client = VLDeviceMqttClient("console.viralink.io", "A1_TEST_TOKEN")
client.connect()
client.subscribe_to_attribute("uploadFrequency", on_attributes_change)
client.subscribe_to_all_attributes(on_attributes_change)
while True:
  time.sleep(1)
```

##### HTTP
Note: The HTTP API only allows a subscription to updates for all attribute.

```python
from vl_device_http import VLHTTPClient

client = VLHTTPClient('https://console.viralink.io', 'secret-token')


def callback(data):
  print(data)
  # ...


# Subscribe
client.subscribe('attributes', callback)
# Unsubscribe
client.unsubscribe('attributes')
```

#### Telemetry pack sending
##### MQTT

```python
import logging
from vl_device_mqtt import VLDeviceMqttClient, VLPublishInfo
import time

telemetry_with_ts = {"ts": int(round(time.time() * 1000)), "values": {"temperature": 42.1, "humidity": 70}}
client = VLDeviceMqttClient("console.viralink.io", "A1_TEST_TOKEN")
# we set maximum amount of messages sent to send them at the same time. it may stress memory but increases performance
client.max_inflight_messages_set(100)
client.connect()
results = []
result = True
for i in range(0, 100):
  results.append(client.send_telemetry(telemetry_with_ts))
for tmp_result in results:
  result &= tmp_result.get() == VLPublishInfo.VL_ERR_SUCCESS
print("Result " + str(result))
client.disconnect()
```
##### HTTP
Unsupported, the HTTP API does not allow the packing of values.

#### Request attributes from server
##### MQTT

```python
import logging
import time
from vl_device_mqtt import VLDeviceMqttClient


def on_attributes_change(client, result, exception):
  if exception is not None:
    print("Exception: " + str(exception))
  else:
    print(result)

client = VLDeviceMqttClient("console.viralink.io", "A1_TEST_TOKEN")
client.connect()
client.request_attributes(["configuration", "targetFirmwareVersion"], callback=on_attributes_change)
while True:
  time.sleep(1)
```
##### HTTP

```python
from vl_device_http import VLHTTPClient

client = VLHTTPClient('https://console.viralink.io', 'secret-token')

client_keys = ['attr1', 'attr2']
shared_keys = ['shared1', 'shared2']
data = client.request_attributes(client_keys=client_keys, shared_keys=shared_keys)
```

#### Respond to server RPC call
##### MQTT

```python
import psutil
import time
import logging
from vl_device_mqtt import VLDeviceMqttClient


# dependently of request method we send different data back
def on_server_side_rpc_request(client, request_id, request_body):
  print(request_id, request_body)
  if request_body["method"] == "getCPULoad":
    client.send_rpc_reply(request_id, {"CPU percent": psutil.cpu_percent()})
  elif request_body["method"] == "getMemoryUsage":
    client.send_rpc_reply(request_id, {"Memory": psutil.virtual_memory().percent})


client = VLDeviceMqttClient("console.viralink.io", "A1_TEST_TOKEN")
client.set_server_side_rpc_request_handler(on_server_side_rpc_request)
client.connect()
while True:
  time.sleep(1)
```

##### HTTP

```python
from vl_device_http import VLHTTPClient

client = VLHTTPClient('https://console.viralink.io', 'secret-token')


def callback(data):
  rpc_id = data['id']
  # ... do something with data['params'] and data['method']...
  response_params = {'result': 1}
  client.send_rpc(name='rpc_response', rpc_id=rpc_id, params=response_params)


# Subscribe
client.subscribe('rpc', callback)
# Unsubscribe
client.unsubscribe('rpc')
```

## Using Gateway APIs

**VLGatewayMqttClient** extends **VLDeviceMqttClient**, thus has access to all it's APIs as a regular device.
Besides, gateway is able to represent multiple devices connected to it. For example, sending telemetry or attributes on behalf of other, constrained, device. See more info about the gateway here: 
#### Telemetry and attributes sending

```python
import time
from vl_gateway_mqtt import VLGatewayMqttClient

gateway = VLGatewayMqttClient("console.viralink.io", "GATEWAY_TEST_TOKEN")
gateway.connect()
gateway.gw_connect_device("Test Device A1")

gateway.gw_send_telemetry("Test Device A1", {"ts": int(round(time.time() * 1000)), "values": {"temperature": 42.2}})
gateway.gw_send_attributes("Test Device A1", {"firmwareVersion": "2.3.1"})

gateway.gw_disconnect_device("Test Device A1")
gateway.disconnect()
```
#### Request attributes

```python
import logging
import time
from vl_gateway_mqtt import VLGatewayMqttClient


def callback(result, exception):
  if exception is not None:
    print("Exception: " + str(exception))
  else:
    print(result)


gateway = VLGatewayMqttClient("console.viralink.io", "TEST_GATEWAY_TOKEN")
gateway.connect()
gateway.gw_request_shared_attributes("Test Device A1", ["temperature"], callback)

while True:
  time.sleep(1)
```
#### Respond to RPC

```python
import time

from vl_gateway_mqtt import VLGatewayMqttClient
import psutil


def rpc_request_response(client, request_id, request_body):
  # request body contains id, method and other parameters
  print(request_body)
  method = request_body["data"]["method"]
  device = request_body["device"]
  req_id = request_body["data"]["id"]
  # dependently of request method we send different data back
  if method == 'getCPULoad':
    gateway.gw_send_rpc_reply(device, req_id, {"CPU load": psutil.cpu_percent()})
  elif method == 'getMemoryLoad':
    gateway.gw_send_rpc_reply(device, req_id, {"Memory": psutil.virtual_memory().percent})
  else:
    print('Unknown method: ' + method)


gateway = VLGatewayMqttClient("console.viralink.io", "TEST_GATEWAY_TOKEN")
gateway.connect()
# now rpc_request_response will process rpc requests from servers
gateway.gw_set_server_side_rpc_request_handler(rpc_request_response)
# without device connection it is impossible to get any messages
gateway.gw_connect_device("Test Device A1")
while True:
  time.sleep(1)
```
## Other Examples

There are more examples for both [device](https://github.com/viralinkio/viralink-python-client-sdk/tree/master/examples/device) and [gateway](https://github.com/viralinkio/viralink-python-client-sdk/tree/master/examples/gateway) in corresponding [folders](https://github.com/viralinkio/viralink-python-client-sdk/tree/master/examples).

## Support

 - [Telegram](https://t.me/viraLinkDiscussion)

## Licenses

This project is released under [Apache 2.0 License](./LICENSE).
