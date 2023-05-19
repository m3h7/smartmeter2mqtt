# Smartmeter to MQTT

Reads from smartmeter and sends obis messages to MQTT.

## Local development

- Linux

```shell
git clone git@github.com:m3h7/smartmeter2mqtt.git
cd smartmeter2mqtt
./test.sh
. .venv/bin/activate
python3 setup.py develop
smartmeter2mqtt -h
```
