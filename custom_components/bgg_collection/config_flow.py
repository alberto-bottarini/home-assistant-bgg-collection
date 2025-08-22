import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

DOMAIN = "bgg_collection"

@config_entries.HANDLERS.register(DOMAIN)
class BggCollectionConfigFlow(config_entries.ConfigFlow):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            username = user_input.get("username")
            if username:
                return self.async_create_entry(title=username, data=user_input)
            else:
                errors["username"] = "required"
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("username"): str,
            }),
            errors=errors,
        )