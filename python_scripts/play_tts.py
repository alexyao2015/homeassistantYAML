def main():
    media_player = data.get("media_player")
    tts_service = data.get("tts_service")
    tts_speak_entity = data.get("tts_speak_entity")
    message = data.get("media_player")

    if not all([media_player, tts_service, message]):
        logger.error(f"Not all required parameters were provided. media_player: {media_player}, tts_service: {tts_service}, message: {message}")
        return

    service_data = {
        "data": {
            "message": message
        }
    }
    
    if tts_service == "speak":
        if not tts_speak_entity
            logger.error("tts_speak_entity must be provided if tts_service == speak")
            return
        service_data["target"]["entity_id"] = tts_speak_entity
        service_data["data"]["media_player_entity_id"] = media_player
        service_data["data"]["cache"] = False
    else:
        service_data["entity_id"] = media_player
        service_data["data"]["cache"] = True

    hass.services.call("tts", tts_service, service_data)

main()
