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

Example:

Message:
`20;83;Oregon Rain2;ID=2a19;RAIN=002a;RAINTOT=0054;BAT=OK;`

is translated to following topics:

- `rflink/Oregon Rain2/2a19/R/RAIN 002a`

- `rflink/Oregon Rain2/2a19/R/RAINTOT 0054`

- `rflink/Oregon Rain2/2a19/R/BAT OK`


Every message received on particular MQTT topic is translated to
RFLink Gateway and sent to 433 MHz.

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
  "mqtt_prefix": "rflink",
  "rflink_tty_device": "/dev/ttyUSB0",
  "rflink_direct_output_params": ["BAT", "CMD", "SET_LEVEL", "SWITCH", "HUM", "CHIME", "PIR", "SMOKEALERT"],
  "rflink_ignored_devices": ["CD23", "12EA"]
}
```

Config param | Meaning
-------------|---------
| mqtt_host | MQTT broker host |
| mqtt_port | MQTT broker port |
| mqtt_prefix | Prefix for publish and subscribe topic (no slash at the end) |
| rflink_tty_device | RFLink tty device |
| rflink_direct_output_params | Parameters transferred to MQTT without any processing |
| rflink_ignored_devices | Devices not taken into account (for both read and write) |

Output data
----------------------
Application pushes informations to MQTT broker in following format:
[mqtt_prefix]/[device_type]/[device_id]/R/[parameter]

`rflink/TriState/8556a8/W/1 OFF`

Every change should be published to topic:
[mqtt_prefix]/[device_type]/[device_id]/W/[switch_ID]

`rflink/TriState/8556a8/W/1 ON`

References
----------------------
- RFLink Gateway project http://www.nemcon.nl/blog2/
- RFLink Gateway protocol http://www.nemcon.nl/blog2/protref
