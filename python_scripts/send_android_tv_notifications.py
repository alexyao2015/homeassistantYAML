services = data.get("services")  # type: list
image_url = data.get("image_url")
title = data.get("title")
message = data.get("message")

if services and message:
    for service in services:
        # domain should always be notify
        domain, service_name = service.split(".")
        service_data = {"message": message}
        if image_url:
            service_data["data"] = {"image": {"url": image_url}}
        if title:
            service_data["title"] = title
        hass.services.call(domain, service_name, service_data)
else:
    logger.error(f"Not all required parameters were provided. message: {message}, title: {title}, image_url: {image_url}, services: {services}")
