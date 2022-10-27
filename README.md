# Smartmeter to MQTT
Reads from smartmeter end send obis messages to MQTT.

## Local development

- Linux

```
git clone git@github.com:m3h7/smartmeter2mqtt.git
cd smartmeter2mqtt
./test.sh
. .venv/bin/activate
python3 setup.py develop
mqtt2influxdb -h
```
