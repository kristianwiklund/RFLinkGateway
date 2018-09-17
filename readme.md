RFLink Gateway to MQTT
======================

Purpose
----------------------
Bridge between RFLink Gateway and MQTT broker.

Current features
----------------------
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

Configuration
----------------------

In order to start the gateway, a few parameters could be set, as ENV variables:

Env variable | Meaning | Default value
-------------|---------|---------
| RFLINK_CONF_FILE | The absolute path to the configuration (config.json) file | Default to config.json |
| RFLINK_LOG_LEVEL | Default log level | Default to 'INFO' |
| RFLINK_FILE_LOG_LEVEL | Log level for the file appender | Default to 'INFO' |
| RFLINK_STREAM_LOG_LEVEL | Log level for the stream appender | Default to 'INFO' |
| RFLINK_LOG_FILE | Path to the log file (file appender) | /var/log/RFLinkGateway.log |


Then, the configuration of the gateway itself can be defined in the JSON configuration file:

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
  "rflink_direct_output_params": ["BAT", "CMD", "SET_LEVEL", "SWITCH", "HUM", "HSTATUS", "CHIME", "PIR", "SMOKEALERT"],
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
| rflink_direct_output_params | Parameters transferred to MQTT without any processing |
| rflink_ignored_devices | Devices not taken into account (for both read and write). Values can be: devices id, family values or 'family/device' couples |

Output data
----------------------
Application pushes informations to MQTT broker in following format:
[mqtt_prefix]/[device_type]/[device_id]/R/[parameter]

`rflink/TriState/8556a8/R/1 OFF`

Every change should be published to topic:
[mqtt_prefix]/[device_type]/[device_id]/W/[switch_ID]

`rflink/TriState/8556a8/W/1 ON`


Special Control Commands
----------------------

It is now possible to send Special Control Command (aka SCC) (ex. 10;PING) to $mqtt_prefix/_COMMAND/IN and receive the response on $mqtt_prefix/_COMMAND/OUT.


References
----------------------
- RFLink Gateway project http://www.nemcon.nl/blog2/
- RFLink Gateway protocol http://www.nemcon.nl/blog2/protref
