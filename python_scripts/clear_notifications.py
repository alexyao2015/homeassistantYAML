for notif in hass.states.entity_ids("persistent_notification"):
    if "frigate_" not in notif:
        continue
    tm_diff = dt_util.utcnow() - hass.states.get(notif).last_changed
    if tm_diff.days > 0:
        hass.services.call(
            "persistent_notification",
            "dismiss",
            {"notification_id": notif.split(".")[1]},
        )
