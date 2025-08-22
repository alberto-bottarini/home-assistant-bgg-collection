import logging
import xml.etree.ElementTree as ET
import asyncio
import aiohttp
from homeassistant.helpers.entity import Entity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

BGG_BOARDGAME_COLLECTION_URL = "https://boardgamegeek.com/xmlapi2/collection?username={username}&stats=1&own=1&subtype=boardgame&excludesubtype=boardgameexpansion"
BGG_BOARDGAMEEXPANSION_COLLECTION_URL = "https://boardgamegeek.com/xmlapi2/collection?username={username}&stats=1&subtype=boardgameexpansion&own=1"

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    username = entry.data.get("username")
    async_add_entities([BggCollectionSensor(hass, username)])

class BggCollectionSensor(Entity):
    def __init__(self, hass, username):
        self._hass = hass
        self._username = username
        self._boardgame_count = None
        self._expansion_count = None
        self._state = None

    @property
    def name(self):
        return f"BGG Collection"

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return {
            "expansions": self._expansion_count,
            'games' : self._boardgame_count,
        }

    async def async_update(self):
        bg_url = BGG_BOARDGAME_COLLECTION_URL.format(username=self._username)
        bge_url = BGG_BOARDGAMEEXPANSION_COLLECTION_URL.format(username=self._username)
        _LOGGER.info(f"[BGG] Requesting urls: {bg_url} {bge_url}")
        try:
            async with aiohttp.ClientSession() as session:
                for _ in range(5): 
                    async with session.get(bg_url) as resp:
                        if resp.status == 200:
                            text = await resp.text()
                            root = ET.fromstring(text)
                            self._boardgame_count = len(root.findall("item"))
                            break
                        elif resp.status == 202:
                            _LOGGER.warning(f"[BGG] Data not ready for url: {bg_url}, retrying...")
                            await asyncio.sleep(5)
                        else:
                            _LOGGER.error(f"[BGG] Download error for url: {bg_url} {resp.status}")
                            return
                for _ in range(5):
                    async with session.get(bge_url) as resp:
                        if resp.status == 200:
                            text = await resp.text()
                            root = ET.fromstring(text)
                            self._expansion_count = len(root.findall("item"))
                            break
                        elif resp.status == 202:
                            _LOGGER.warning(f"[BGG] Data not ready for url: {bge_url}, retrying...")
                            await asyncio.sleep(5) 
                        else:
                            _LOGGER.error(f"[BGG] Download error for url: {bge_url} {resp.status}")
                            return

                self._state = self._boardgame_count + self._expansion_count
            _LOGGER.info(f"[BGG] Collection updated: {self._boardgame_count} board games, {self._expansion_count} expansions")
        except Exception as e:
            _LOGGER.error(f"[BGG] Generic Error: {e}")