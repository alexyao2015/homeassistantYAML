"""Persistent Notification Prune Component."""
from __future__ import annotations

from datetime import datetime, timedelta

from homeassistant.components.persistent_notification import (
    _async_get_or_create_notifications,
    async_dismiss,
    ATTR_CREATED_AT
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall, callback

DOMAIN = "persistent_notification_prune"

OLDEST_NOTIFICATION_DAYS = 1
SERVICE_NAME = "dismiss_old_notifications"

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Setup the service."""

    @callback
    def dismiss_old_notifications(call: ServiceCall) -> None:
        """Handle the dismiss notification service call."""
        id_filter = call.data.get("notification_id_filter")

        oldest_date = datetime.now() - timedelta(days=call.data.get("keep_days", OLDEST_NOTIFICATION_DAYS))

        dismiss_ids = []
        notifications = _async_get_or_create_notifications(hass)
        for notification_id, notification in notifications.copy().items():
            if id_filter is not None and id_filter not in notification_id:
                continue

            created_date: datetime = notification[ATTR_CREATED_AT]
            if created_date.timestamp() < oldest_date.timestamp():
                dismiss_ids.append(notification_id)
        for dismiss_id in dismiss_ids:
            async_dismiss(hass, dismiss_id)

    hass.services.async_register(
        DOMAIN,
        SERVICE_NAME,
        dismiss_old_notifications,
        None,
    )
    return True

async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    hass.services.async_remove(
        DOMAIN,
        SERVICE_NAME,
    )
    return True
