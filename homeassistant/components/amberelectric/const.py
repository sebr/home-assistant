"""Amber Electric Constants."""

from enum import StrEnum
import logging

from homeassistant.const import Platform

DOMAIN = "amberelectric"
CONF_SITE_NAME = "site_name"
CONF_SITE_ID = "site_id"
CONF_PRICE_RESOLUTION = "price_resolution"
CONF_PRICE_FORECAST_NEXT = "price_forecast_next"


class ConfPriceResolution(StrEnum):
    """Price resolution options."""

    FIVE_MIN = "5_MINUTES"
    THIRTY_MIN = "30_MINUTES"


ATTRIBUTION = "Data provided by Amber Electric"

LOGGER = logging.getLogger(__package__)
PLATFORMS = [Platform.BINARY_SENSOR, Platform.SENSOR]
