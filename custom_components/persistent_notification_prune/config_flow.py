"""Config flow for the persistent_notification_prune component."""
import secrets

from homeassistant import config_entries


class PersistentNotificationPruneConfigFlow(
    config_entries.ConfigFlow, domain="persistent_notification_prune"
):
    """Config flow for persistent_notification_prune."""

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""

        # Only a single instance of the integration
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        conf_id = secrets.token_hex(6)

        await self.async_set_unique_id(conf_id)
        self._abort_if_unique_id_configured(updates=user_input)

        return self.async_create_entry(title="Persistent Notification Prune", data={})
