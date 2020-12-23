
from fastapi import APIRouter, Request, Response
from loguru import logger
from .middlewares.verification import DiscordVerificationMiddleware
from .models.incoming import IncomingDiscordInteraction
from .eventer import EventHandler
import json

router = APIRouter()
interaction = EventHandler()

@router.post("/interactions")
async def handle_interactions(request: Request) -> Response:
    logger.info("interaction recieved.")
    

    _get_request_body = json.loads(request.state._cached_body.decode())
    if _get_request_body['type'] == 1:
        logger.info("handling ACK Ping.")
        return {
            "type": 1
        }
    
    _parse_to_object = IncomingDiscordInteraction(**_get_request_body)
    return await interaction.emit(_parse_to_object.data.name, payload=_parse_to_object)

    