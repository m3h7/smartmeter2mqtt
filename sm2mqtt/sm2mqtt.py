import logging
import os
import re
import paho.mqtt.client


class Smartmeter2Mqtt:
    def __init__(self, config):
        self._config = config

        self._device = open(config['smartmeter']['device'], 'r')

        self._mqtt = paho.mqtt.client.Client()

        if config['mqtt'].get('username', None):
            self._mqtt.username_pw_set(config['mqtt']['username'], config['mqtt'].get('password', None))

        if config['mqtt'].get('cafile', None):
            self._mqtt.tls_set(config['mqtt']['cafile'],
                               config['mqtt'].get('certfile', None),
                               config['mqtt'].get('keyfile', None))

        self._mqtt.on_connect = self._on_mqtt_connect
        self._mqtt.on_disconnect = self._on_mqtt_disconnect
        self._mqtt.on_publish = self._on_mqtt_publish

        self._mqtt_topic_prefix = f"smartmeter/{config['mqtt'].get('topic_prefix', '0')}/"

    def _on_mqtt_connect(self, client, userdata, flags, rc):
        logging.info('Connected to MQTT broker with code %s', rc)

        lut = {paho.mqtt.client.CONNACK_REFUSED_PROTOCOL_VERSION: 'incorrect protocol version',
               paho.mqtt.client.CONNACK_REFUSED_IDENTIFIER_REJECTED: 'invalid client identifier',
               paho.mqtt.client.CONNACK_REFUSED_SERVER_UNAVAILABLE: 'server unavailable',
               paho.mqtt.client.CONNACK_REFUSED_BAD_USERNAME_PASSWORD: 'bad username or password',
               paho.mqtt.client.CONNACK_REFUSED_NOT_AUTHORIZED: 'not authorised'}

        if rc != paho.mqtt.client.CONNACK_ACCEPTED:
            logging.error('mqtt: Connection refused from reason: %s', lut.get(rc, 'unknown code'))

    def _on_mqtt_disconnect(self, client, userdata, rc):
        logging.info('mqtt: Disconnect from MQTT broker with code %s', rc)

    def _on_mqtt_publish(self, client, userdata, mid):
        logging.debug(f'mqtt: Published: {mid}')

    def run(self):
        logging.info("Run it")

        self._mqtt.connect(self._config['mqtt']['host'], self._config['mqtt']['port'], keepalive=10)
        self._mqtt.loop_start()

        while True:
            line = self._device.readline()
            if not line:
                break

            logging.debug(line)

            # 1-0:1.8.0*255(008761.7115*kWh)
            msg = re.search(r'(.*)\((.*)\*(.*)\)', line)
            if not msg:
                logging.debug('Line ignored')
                continue

            (key, value, unit) = msg.group(1, 2, 3)
            value = self.format_value(value)
            topic = self._mqtt_topic_prefix + self.format_key(key)

            logging.debug(f'Topic: {topic} Value: {value} Unit: {unit}')

            self._mqtt.publish(topic, value)

    @staticmethod
    def format_value(value):
        # remove leain zero's from value
        if value[0] == '0':
            value = value.lstrip('0')
        elif value[0] == '-':
            value = '-' + value.lstrip('-').lstrip('0')

        # value is '0', but all removed
        if len(value) == 0:
            value = '0'

        # adds a '0' to value < 0
        if value[0] == '.':
            value = '0' + value

        return value

    @staticmethod
    def format_key(key):
        key = key.replace('*', '_')
        return key
