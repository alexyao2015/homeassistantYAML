"""Config flow for the frigate_uploader component."""

from slugify import slugify
import voluptuous as vol

from homeassistant.components.frigate_uploader.const import ATTR_FRIGATE_URL, DOMAIN
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult


class FrigateUploaderConfigFlow(ConfigFlow, domain=DOMAIN):
    """Config flow for frigate_uploader."""

    async def async_step_user(self, user_input=None) -> ConfigFlowResult:
        """Handle a flow initialized by the user."""
        if user_input is None:
            user_input = {}

        frigate_url = user_input.get(ATTR_FRIGATE_URL, "")
        if frigate_url:
            return self.async_create_entry(
                title=slugify(user_input[ATTR_FRIGATE_URL]), data=user_input
            )

        return self.async_show_form(
            data_schema=vol.Schema(
                {
                    vol.Required(
                        ATTR_FRIGATE_URL,
                        default=frigate_url,
                    ): str,
                }
            ),
        )
