for notif in hass.states.entity_ids("persistent_notification"):
    if "frigate" not in notif:
        continue
    tm_diff = dt_util.utcnow() - hass.states.get(notif).last_changed
    if tm_diff.seconds >= 86400:
        hass.services.call(
            "persistent_notification",
            "dismiss",
            {"notification_id": notif.split(".")[1]},
        )
