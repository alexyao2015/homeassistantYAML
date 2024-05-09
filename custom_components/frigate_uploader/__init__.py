"""Frigate Uploader Component."""

from __future__ import annotations

from asyncio import timeout
from functools import partial
import json
import logging

import aiohttp
from aiohttp import ClientResponseError

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import aiohttp_client

from .const import ATTR_FRIGATE_URL, DOMAIN, SERVICE_NAME_UPLOAD_TO_FRIGATE_PLUS

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Setup the service."""

    hass.services.async_register(
        DOMAIN,
        SERVICE_NAME_UPLOAD_TO_FRIGATE_PLUS,
        partial(upload_to_frigate_plus, hass, entry.data[ATTR_FRIGATE_URL]),
        None,
    )
    return True


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    hass.services.async_remove(
        DOMAIN,
        SERVICE_NAME_UPLOAD_TO_FRIGATE_PLUS,
    )
    return True


async def upload_to_frigate_plus(
    hass: HomeAssistant, frigate_url: str, call: ServiceCall
) -> None:
    event_id = call.data["frigate_event_id"]
    try:
        session = aiohttp_client.async_get_clientsession(hass)
        async with timeout(30):
            response = await session.post(
                f"{frigate_url}/api/events/{event_id}/plus",
                data=json.dumps({"include_annotation": 0}),
                allow_redirects=True,
            )
            response.raise_for_status()
            _LOGGER.debug("Uploaded event %s to frigate plus", event_id)
    except (TimeoutError, aiohttp.ClientError, ClientResponseError) as ex:
        _LOGGER.error("Error uploading: %s", ex)
        return None
