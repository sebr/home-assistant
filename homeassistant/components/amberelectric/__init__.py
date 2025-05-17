"""Support for Amber Electric."""

import logging

import amberelectric

from homeassistant.const import CONF_API_TOKEN
from homeassistant.core import HomeAssistant

from .const import (
    CONF_PRICE_FORECAST_NEXT,
    CONF_PRICE_RESOLUTION,
    CONF_SITE_ID,
    PLATFORMS,
    ConfPriceResolution,
)
from .coordinator import AmberConfigEntry, AmberUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: AmberConfigEntry) -> bool:
    """Set up Amber Electric from a config entry."""
    configuration = amberelectric.Configuration(access_token=entry.data[CONF_API_TOKEN])
    api_client = amberelectric.ApiClient(configuration)
    api_instance = amberelectric.AmberApi(api_client)
    site_id = entry.data[CONF_SITE_ID]

    _LOGGER.debug("async_setup_entry: data: %s options: %s", entry.data, entry.options)

    resolution_map = {
        ConfPriceResolution.FIVE_MIN: 5,
        ConfPriceResolution.THIRTY_MIN: 30,
    }
    price_resolution = resolution_map.get(
        entry.options.get(CONF_PRICE_RESOLUTION, ConfPriceResolution.THIRTY_MIN)
    )

    price_forecast_next = entry.options.get(CONF_PRICE_FORECAST_NEXT, 48)

    coordinator = AmberUpdateCoordinator(
        hass, entry, api_instance, site_id, price_resolution, price_forecast_next
    )
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator
    entry.async_on_unload(entry.add_update_listener(update_listener))

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def update_listener(hass: HomeAssistant, entry: AmberConfigEntry) -> None:
    """Handle options update."""
    _LOGGER.debug(
        "async_update_options: data: %s options: %s", entry.data, entry.options
    )
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: AmberConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
