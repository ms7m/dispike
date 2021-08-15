from fastapi import APIRouter, Request, Response
from fastapi.responses import PlainTextResponse
from loguru import logger

from .incoming.incoming_interactions import IncomingDiscordUserCommandInteraction, \
    IncomingDiscordMessageCommandInteraction
from .middlewares.verification import DiscordVerificationMiddleware
from dispike.incoming import (
    IncomingDiscordSlashInteraction,
    IncomingDiscordSlashData,
    SubcommandIncomingDiscordOptionList,
    IncomingDiscordOption,
    IncomingDiscordButtonInteraction,
    IncomingDiscordSelectMenuInteraction, Member, Message
)
from .eventer import EventTypes
from .eventer_helpers.determine_event_information import determine_event_information
from .response import DiscordResponse, DeferredResponse, DeferredEmphericalResponse
from dispike.creating.components import ComponentTypes
import json
import typing
import asyncio
import warnings


if typing.TYPE_CHECKING:
    from .main import Dispike

router = APIRouter()
router._dispike_instance = None
interaction = router._dispike_instance  # type: Dispike


_RAISE_FOR_TESTING = False


async def _run_and_log_async(coroutine: typing.Coroutine) -> None:
    logger.debug(f"Incoming deferred coroutine.. {coroutine}")
    await coroutine
    logger.debug(f"Deferred coroutine completed!")


@router.get("/ping")
async def ping():
    return PlainTextResponse(
        "If you see this, Your instance is working and accepting requests."
    )


@router.post("/interactions")
async def handle_interactions(request: Request) -> Response:
    if router._dispike_instance == None:
        return PlainTextResponse(
            "If you see this, Dispike has not been properly configured. Make sure to create a Dispike instance before starting this endpoint."
        )

    logger.info("interaction recieved.")

    _get_request_body = json.loads(request.state._cached_body.decode())
    logger.info(_get_request_body)
    if _get_request_body["type"] == 1:
        logger.info("handling ACK Ping.")
        return {"type": 1}

    if _get_request_body["type"] == 2:
        # ["data"]["type"] represents if its a message or user command

        if _get_request_body["data"]["type"] == 2:
            # 2 is user command

            _parse_to_object = IncomingDiscordUserCommandInteraction(
                **_get_request_body
            )

            # Confusingly construct a member object
            _member = Member(
                **{
                    **_get_request_body["data"]["resolved"]["members"][
                        _parse_to_object.data.target_id
                    ],
                    "user": {
                        **_get_request_body["data"]["resolved"]["users"][
                            _parse_to_object.data.target_id
                        ]
                    },
                }
            )

            # Set that member object as the target
            _parse_to_object.data.__setattr__("target", _member)

            _get_res = await router._dispike_instance.emit(
                _get_request_body["data"]["name"],
                EventTypes.USER_COMMAND,
                _parse_to_object,
            )
            return _get_res.response
        elif _get_request_body["data"]["type"] == 3:
            # 3 is message command

            _parse_to_object = IncomingDiscordMessageCommandInteraction(
                **_get_request_body
            )

            _message = Message(
                **_get_request_body["data"]["resolved"]["messages"][
                    _parse_to_object.data.target_id
                ]
            )

            # Set that message object as the target
            _parse_to_object.data.__setattr__("target", _message)

            _get_res = await router._dispike_instance.emit(
                _get_request_body["data"]["name"],
                EventTypes.MESSAGE_COMMAND,
                _parse_to_object,
            )
            return _get_res.response

    if _get_request_body["type"] == 3:
        if _get_request_body["data"]["component_type"] == ComponentTypes.BUTTON.value:
            # Button
            _parse_to_object = IncomingDiscordButtonInteraction(**_get_request_body)

            _get_res = await router._dispike_instance.emit(
                _get_request_body["data"]["custom_id"],
                EventTypes.COMPONENT,
                _parse_to_object,
            )
            return _get_res.response
        if (
            _get_request_body["data"]["component_type"]
            == ComponentTypes.SELECT_MENU.value
        ):
            # Select Menu
            _parse_to_object = IncomingDiscordSelectMenuInteraction(**_get_request_body)

            _get_res = await router._dispike_instance.emit(
                _get_request_body["data"]["custom_id"],
                EventTypes.COMPONENT,
                _parse_to_object,
            )
            return _get_res.response

    _parse_to_object = IncomingDiscordSlashInteraction(**_get_request_body)
    _event_name, arguments = determine_event_information(_parse_to_object)
    logger.debug(f"incoming event name: {_event_name}")
    if not router._dispike_instance.check_event_exists(_event_name, EventTypes.COMMAND):
        logger.debug("discarding event not existing.")
        warnings.warn(
            f"Event {_event_name} does not exist or does not have a callback.",
            UserWarning,
        )
        return {"type": 5}

    # _event_settings = router._dispike_instance.return_event_settings(_event_name)

    arguments[router._user_defined_setting_ctx_value] = _parse_to_object

    # Check the type hint for the return type, fallback for checking the type if no hints are provided
    try:
        _type_hinted_request = router._dispike_instance.view_event_function_return_type(
            _event_name, EventTypes.COMMAND
        )
        _type_hinted_returned_value = _type_hinted_request["return"]
        if _type_hinted_returned_value == DiscordResponse:
            _get_res = await router._dispike_instance.emit(
                _event_name, EventTypes.COMMAND, **arguments
            )

            logger.debug(_get_res.response)
            return _get_res.response
        elif (
            _type_hinted_returned_value == DeferredResponse
            or _type_hinted_returned_value == DeferredEmphericalResponse
        ):
            logger.debug("This is a deferred response...")

            asyncio.create_task(
                _run_and_log_async(
                    router._dispike_instance.emit(
                        _event_name, EventTypes.COMMAND, **arguments
                    )
                )
            )
            return _type_hinted_returned_value.response

        elif _type_hinted_returned_value == dict:
            return await router._dispike_instance.emit(
                _event_name, EventTypes.COMMAND, **arguments
            )
    except KeyError:
        logger.error(
            "unable to find return value for type hint.. resorting to guessing.."
        )
        if _RAISE_FOR_TESTING:
            raise AssertionError("No hinting!")  # pragma: no cover
    except Exception:
        logger.exception("unhandled exception for returning hinted value")
        raise

    interaction_data = await router._dispike_instance.emit(
        _event_name, EventTypes.COMMAND, **arguments
    )
    if isinstance(interaction_data, DiscordResponse):
        interaction_data: DiscordResponse
        return interaction_data.response

    if isinstance(interaction_data, dict):
        return interaction_data

    warnings.warn(
        f"Command {_event_name} has not been configured with a valid callback function.",
        UserWarning,
    )
    logger.warning(
        f"Command {_event_name} has not been configured with a valid callback function."
    )

    # Backup response, simply acknowledge. (Type 5)
    return DiscordResponse(
        content="**Warning**: This command has not been configured. (sent by dispike)",
        empherical=True,
    )
