services = data.get("services")  # type: list
image_url = data.get("image_url")
title = data.get("title")
message = data.get("message")

if services and image_url and title and message:
    for service in services:
        service_data = {"message": message, "title": title, "data": {"image": {"url": image_url}}}
        hass.services.call("notify", service, service_data)
else:
    logger.error(f"Not all required parameters were provided. message: {message}, title: {title}, image_url: {image_url}, services: {services}")
