"""
Example of a custom MQTT component.
Shows how to communicate with MQTT. Follows a topic on MQTT and updates the
state of an entity to the last message received on that topic.
Also offers a service 'set_state' that will publish a message on the topic that
will be passed via MQTT to our message received listener. Call the service with
example payload {"new_state": "some new state"}.
Configuration:
To use the mqtt_example component you will need to add the following to your
configuration.yaml file.
mqtt_basic_async:
  topic: "home-assistant/mqtt_example"
"""
from __future__ import annotations

import voluptuous as vol

from homeassistant.components import mqtt
from homeassistant.core import HomeAssistant, ServiceCall, callback
from homeassistant.helpers.typing import ConfigType

# The domain of your component. Should be equal to the name of your component.
from .const import DOMAIN

# Schema to validate API KEY
CONFIG_SCHEMA = vol.Schema({
    vol.Required(CONF_API_KEY): cv.string
})

async def get(url):
    response = await loop.run_in_executor(executor, requests.get, url)
    return response.text

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the MQTT async example component."""
    topic = config[DOMAIN][CONF_TOPIC]
    entity_id = 'mqtt_example.last_message'

    # Listen to a message on MQTT.
    @callback
    def message_received(topic: str, payload: str, qos: int) -> None:
        """A new MQTT message has been received."""
        hass.states.async_set(entity_id, payload)

    await hass.components.mqtt.async_subscribe(topic, message_received)

    hass.states.async_set(entity_id, 'No messages')

    # Service to publish a message on MQTT.
    @callback
    def set_state_service(call: ServiceCall) -> None:
        """Service to send a message."""
        hass.components.mqtt.async_publish(topic, call.data.get('new_state'))

    # Register our service with Home Assistant.
    hass.services.async_register(DOMAIN, 'set_state', set_state_service)

    # Return boolean to indicate that initialization was successfully.
    return True