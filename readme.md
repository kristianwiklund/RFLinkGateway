# RFLink Gateway to MQTT

## IMPORTANT

Python 3 only

## Purpose

Bridge between RFLink Gateway and MQTT broker.

## Current features

Forwarding messages received on TTY port from RFLink Gateway Arduino board
to MQTT broker in both directions.

Every message received from RFLinkGateway is split into single parameters
and published to different MQTT topics.

Examples:

Message:
`20;83;Oregon Rain2;ID=2a19;RAIN=002a;RAINTOT=0054;BAT=OK;`

is translated to following topics:

- `rflink/Oregon Rain2/2a19/R/RAIN 002a`

- `rflink/Oregon Rain2/2a19/R/RAINTOT 0054`

- `rflink/Oregon Rain2/2a19/R/BAT OK`

The whole message can also be sent on its own topic in addition to the previous behavior:

- `rflink/Oregon Rain2/2a19/R/message 20;83;Oregon Rain2;ID=2a19;RAIN=002a;RAINTOT=0054;BAT=OK;`

Or a JSON formated output can also be used. In this particular case, there is only one message sent to a single topic, but with a more convenient format:

- `rflink/Oregon Rain2/2a19/R/message {"RAIN": "002a", "RAINTOT": "0054", "BAT": "OK"}`

Every message received on particular MQTT topics is transmitted to
RFLink Gateway and sent to the right 433 MHz device.

## Configuration

In order to start the gateway, a few parameters could be set, as ENV variables:

Env variable | Meaning | Default value
-------------|---------|---------
| RFLINK_CONF_FILE | The absolute path to the configuration (config.json) file | Default to config.json |
| RFLINK_LOG_LEVEL | Default log level | Default to 'INFO' |
| RFLINK_FILE_LOG_LEVEL | Log level for the file appender | Default to 'INFO' |
| RFLINK_STREAM_LOG_LEVEL | Log level for the stream appender | Default to 'INFO' |
| RFLINK_LOG_FILE | Path to the log file (file appender) | /var/log/RFLinkGateway.log |


Then, the configuration of the gateway itself can be defined in the JSON configuration file.
**NOTE: Modifications were done. The parameter 'rflink_direct_output_params' no longer exists. It is now replaced by 'rflink_output_params_processing'. Please, pay attention to the updated configuration file below**

```json
{
  "mqtt_host": "your.mqtt.host",
  "mqtt_port": 1883,
  "mqtt_user": "user",
  "mqtt_password": "password",
  "mqtt_prefix": "rflink",
  "mqtt_message_timeout": 60,
  "mqtt_switch_incl_topic": "true",
  "mqtt_json": "true",
  "mqtt_include_message": "false",  
  "rflink_tty_device": "/dev/ttyUSB0",
  "rflink_output_params_processing": {
        "ID": [],
        "SWITCH": [],
        "CMD": [],
        "SET_LEVEL": ["str2dec"],
        "TEMP": ["shex2dec","div10"],
        "HUM": ["str2dec"],
        "BARO": ["hex2dec"],
        "HSTATUS": ["str2dec"],
        "BFORECAST": ["str2dec"],
        "UV": [["hex2dec", "div10"],["hex2dec", "div10", "uv2level"]],
        "LUX": ["hex2dec"],
        "BAT": [],
        "RAIN": ["hex2dec","div10"],
        "RAINRATE": ["hex2dec","div10"],
        "WINSP": ["hex2dec","div10"],
        "AWINSP": ["hex2dec","div10"],
        "WINGS": ["hex2dec","div10"],
        "WINDIR": ["mapdir"],
        "WINCHL": ["shex2dec","div10"],
        "WINTMP": ["shex2dec","div10"],
        "CHIME": ["str2dec"],
        "SMOKEALERT": [],
        "PIR": [],
        "CO2": [],
        "SOUND": ["str2dec"],
        "KWATT": ["hex2dec"],
        "WATT": ["hex2dec"],
        "CURRENT": ["str2dec"],
        "CURRENT2": ["str2dec"],
        "CURRENT3": ["str2dec"],
        "DIST": ["str2dec"],
        "METER": ["str2dec"],
        "VOLT": ["str2dec"],
        "RGBW": [],
        "message": []
  },
  "rflink_ignored_devices": ["CD23", "12EA", "Alecto V4", "Oregon TempHygro/328AB"]
}
```

Config param | Meaning
-------------|---------
| mqtt_host | MQTT broker host |
| mqtt_port | MQTT broker port |
| mqtt_prefix | Prefix for publish and subscribe topic (no slash at the end) |
| mqtt_switch_incl_topic | Include (or not) SWITCH number in the topic name instead of in the payload |
| mqtt_include_message | Send to MQTT the full message (containing all information) in addition to individual informations |
| mqtt_json_format | Format the payload as a JSON string. Act as a pretty convenient alternative to full message + individual infos |
| rflink_tty_device | RFLink tty device |
| rflink_gateway_uri | See pyserial docs for URI formats. Allows connection to e.g. an rflink proxy server. Only used if rflink_tty_device is not present in configuration!
| rflink_output_params_processing | describe how to process received values |
| rflink_ignored_devices | Devices not taken into account (for both read and write). Values can be: devices id, family values or 'family/device' couples |

### How to process received values (rflink_output_params_processing)

Each value can have zero, one or more 'processors'.
When no processor is specified (empty array : ```[]```), the value is sent as is to MQTT.
When processors are defined, they are applied in their natural order.

NEW: processors can be an array of arrays. In this particular case, several different values are returned for the same input. For instance, if you want to have both a numerical value AND a specific label for one input (let's say UV indice where you want the indice and a level, which is a string describing how strong UV level is), you can specify to distinct processing chains, each one in its array: ```"UV": [["hex2dec", "div10"],["hex2dec", "div10", "uv2level"]]```. The first value will be named like the received data, for instance "RAIN": ```rflink/Oregon Rain2/1b19/R/RAIN 6``` and the following derived values will be name using the same prefix ("RAIN" here) and followed by "_ALT_" and an increment starting at 1 ("RAIN_ALT_1", "RAIN_ALT_2", ....).

Available processors are:

* shex2dec : convert a signed hex string to a decimal value
* hex2dec : convert a hex string to a decimal value
* str2dec : convert a string to a decimal value
* div10 : divide the value by 10
* dir2deg : convert a (wind) direction (0-15) to a degree value
* dir2car : convert a (wind) direction (0-15) to a cardinal point (N, E, W, S, NNW, ...)
* uv2level : return a string defining the level of UV depending on the value (values are coming from Oregon documentation: LOW, MED, HI...)
* wind2level : return a string defining the strength of the wind, from Oregon's documentation

NOTE: Processors are declared in Processors.py file.
New processors can be added.
You just have to create a new function and define it in the dictionary, called 'processors', at the end of the file.
If your syntax is Python3 compliant, it should just work! :-)

That way, you can choose how to deal with each possible value.

## Output data

Application pushes informations to MQTT broker in following format:
[mqtt_prefix]/[device_type]/[device_id]/R/[parameter]

`rflink/TriState/8556a8/R/1 OFF`

Every change should be published to topic:
[mqtt_prefix]/[device_type]/[device_id]/W/[switch_ID]

`rflink/TriState/8556a8/W/1 ON`


## Special Control Commands

It is now possible to send Special Control Command (aka SCC) (ex. 10;PING) to $mqtt_prefix/_COMMAND/IN and receive the response on $mqtt_prefix/_COMMAND/OUT.


## References

- RFLink Gateway project http://www.nemcon.nl/blog2/
- RFLink Gateway protocol http://www.nemcon.nl/blog2/protref
