"""A demonstration 'hub' that connects several devices."""
from __future__ import annotations

# In a real implementation, this would be in an external library that's on PyPI.
# The PyPI package needs to be included in the `requirements` section of manifest.json
# See https://developers.home-assistant.io/docs/creating_integration_manifest
# for more information.
# This dummy hub always returns 3 rollers.
import asyncio
import random


class Hub:
    """Tinxy Hub"""

    manufacturer = "Tinxy"

    def __init__(self, hass: HomeAssistant, host: str, api_key: str) -> None:
        """Init dummy hub."""
        self._host = host
        self._hass = hass
        self._name = "Tinxy"
        self._api_key = api_key
        self._id = self._name.lower()
        self.rollers = []
        self.online = True

    @property
    def hub_id(self) -> str:
        """ID for dummy hub."""
        return self._id

    async def load_devices(self):
        

    async def test_connection(self) -> bool:
        """Test connectivity to the Dummy hub is OK."""
        await asyncio.sleep(1)
        return True


class TinxySwitch:
    def __init__(self, api_key, device_id, device_name, relay_no, device_type):
        self.device_name = device_name
        self.relay_no = relay_no
        self.device_id = device_id
        self.type = device_type
        self._is_on = False

        self.url = "https://"+self._host+"/"+self.device_id+"/toggle"
        self.token = "Bearer "+api_key
        self.read_status()
        self.is_available = True

    @property
    def available(self):
        return self.is_available

    @property
    def unique_id(self):
        return self.device_id+'-'+self.relay_no

    @property
    def icon(self) -> str | None:
        """Icon of the entity."""

        if self.type == "Heater":
            return "mdi:radiator"
        elif self.type == "Tubelight":
            return "mdi:lightbulb-fluorescent-tube"
        elif self.type == "LED Bulb" or self.type == "Dimmable Light" or self.type == "LED Dimmable Bulb":
            return "mdi:lightbulb"
        elif self.type == "Music System":
            return "mdi:music"
        elif self.type == "Fan":
            return "mdi:fan"
        elif self.type == "Socket":
            return "mdi:power-socket-eu"
        elif self.type == "TV":
            return "mdi:television"
        else:
            return "mdi:toggle-switch"

    @property
    def name(self):
        """Name of the entity."""
        return self.device_name

    @property
    def should_poll(self):
        return True

    @property
    def is_on(self):
        """If the switch is currently on or off."""
        # self.read_status()
        return self._is_on

    def turn_on(self, **kwargs):
        """Turn the switch on."""

        self._is_on = True
        self.switch_api()

    def turn_off(self, **kwargs):
        """Turn the switch off."""
        self._is_on = False
        self.switch_api()

    def read_status(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": self.token
        }
        try:
            response = requests.request(
                "GET", "https://backend.tinxy.in/v2/devices/"+self.device_id+"/state?deviceNumber="+self.relay_no, data="", headers=headers)
            data = response.json()

            if data["status"] and data["status"] == 1:
                self.is_available = True
            else:
                self.is_available = False

            if data["state"] and data["state"] == "ON":
                self._is_on = True
            elif data["state"] and data["state"] == "OFF":
                self._is_on = False

        except Exception as e:
            self.is_available = False
            _LOGGER.error("Something else happned read_status exception")

    def switch_api(self):

        _LOGGER.warning("switch_api called device_id %s relay_no %s",
                        self.device_id, self.relay_no)
        try:
            payload = {
                "request": {
                    "state": 1 if self._is_on == True else 0
                },
                "deviceNumber": int(self.relay_no) + 1
            }

            headers = {
                "Content-Type": "application/json",
                "Authorization": self.token
            }

            response = requests.request(
                "POST", self.url, data=json.dumps(payload), headers=headers)

            # _LOGGER.warning("switch_api result",response.text)
        except Exception as e:
            self.is_available = False
            # _LOGGER.error("Something else happned read_status %s", e)
