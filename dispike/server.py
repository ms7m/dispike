from fastapi import APIRouter, Request, Response
from fastapi.responses import PlainTextResponse
from loguru import logger
from .middlewares.verification import DiscordVerificationMiddleware
from .models.incoming import IncomingDiscordInteraction
from .eventer import EventHandler
from .response import DiscordResponse, NotReadyResponse
import json
import typing

router = APIRouter()
interaction = EventHandler()


_RAISE_FOR_TESTING = False


@router.get("/ping")
async def ping():
    return PlainTextResponse(
        "If you see this, Your instance is working and accepting requests."
    )


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

    # Check the type hint for the return type, fallback for checking the type if no hints are provided
    try:
        _type_hinted_request = interaction.view_event_function_return_type(
            _parse_to_object.data.name
        )
        _type_hinted_returned_value = _type_hinted_request["return"]
        if _type_hinted_returned_value == DiscordResponse:
            _get_res = await interaction.emit(_parse_to_object.data.name, **arguments)
            return _get_res.response
        elif _type_hinted_returned_value == NotReadyResponse:
            return None
        elif _type_hinted_returned_value == dict:
            return await interaction.emit(_parse_to_object.data.name, **arguments)
    except KeyError:
        logger.error(
            "unable to find return value for type hint.. resorting to guessing.."
        )
        if _RAISE_FOR_TESTING == True:
            raise AssertionError("No hinting!")
    except Exception:
        logger.exception("unhandled exception for returning hinted value")
        raise

    interaction_data = await interaction.emit(_parse_to_object.data.name, **arguments)
    if isinstance(interaction_data, DiscordResponse):
        interaction_data: DiscordResponse
        return interaction_data.response

    if isinstance(interaction_data, dict):
        return interaction_data

    if isinstance(interaction_data, NotReadyResponse):
        return None