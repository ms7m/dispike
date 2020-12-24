from fastapi import APIRouter, Request, Response
from loguru import logger
from .middlewares.verification import DiscordVerificationMiddleware
from .models.incoming import IncomingDiscordInteraction
from .eventer import EventHandler
import json
import typing

router = APIRouter()
interaction = EventHandler()


@router.post("/interactions")
async def handle_interactions(request: Request) -> Response:
    logger.info("interaction recieved.")

    _get_request_body = json.loads(request.state._cached_body.decode())
    logger.info(_get_request_body)
    if _get_request_body["type"] == 1:
        logger.info("handling ACK Ping.")
        return {"type": 1}

    _parse_to_object = IncomingDiscordInteraction(**_get_request_body)

    if interaction.check_event_exists(_parse_to_object.data.name) == False:
        logger.debug("discarding event not existing.")
        return {}

    if len(_parse_to_object.data.options) > 0:
        arguments = {x.name: x.value for x in _parse_to_object.data.options}
    else:
        arguments = {}

    arguments["ctx"] = _parse_to_object

    return await interaction.emit(_parse_to_object.data.name, **arguments)
