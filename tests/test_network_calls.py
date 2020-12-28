from httpx import Response
from dispike.models.incoming import IncomingApplicationCommand
from pytest_httpx import HTTPXMock
from dispike import Dispike

from pydantic import ValidationError
import pytest

from dispike.errors.network import DiscordAPIError
from nacl.encoding import HexEncoder
from nacl.signing import SigningKey

import respx


@pytest.fixture
def dispike_object():
    _generated_signing_key = SigningKey.generate()
    verification_key = _generated_signing_key.verify_key.encode(encoder=HexEncoder)

    return Dispike(
        client_public_key=verification_key.decode(),
        bot_token="BOTTOKEN",
        application_id="APPID",
    )


@respx.mock
def test_get_commands_globally_call_successful(dispike_object: Dispike):
    respx.get(f"https://discord.com/api/v8/applications/APPID/commands").mock(
        return_value=Response(
            200,
            json=[
                {
                    "id": "1234",
                    "application_id": "7890",
                    "name": "mccoolbotv1",
                    "description": "McCoolbot is the coolest bot around.",
                    "options": [
                        {"type": 6, "name": "wave", "description": "wave at a person"}
                    ],
                },
                {
                    "id": "3344",
                    "application_id": "7890",
                    "name": "mccoolbotv2",
                    "description": "send a message",
                    "options": [
                        {"type": 3, "name": "message", "description": "send a message"}
                    ],
                },
            ],
        )
    )

    _get_commands = dispike_object.get_commands()
    for item in _get_commands:
        assert isinstance(item, IncomingApplicationCommand) == True

    assert len(_get_commands) == 2


@respx.mock
def test_get_commands_globally_call_fail(dispike_object: Dispike):
    respx.get("https://discord.com/api/v8/applications/APPID/commands").mock(
        return_value=Response(
            500,
            json=[
                {
                    "id": "1234",
                    "application_id": "7890",
                    "name": "mccoolbotv1",
                    "description": "McCoolbot is the coolest bot around.",
                    "options": [
                        {"type": 6, "name": "wave", "description": "wave at a person"}
                    ],
                },
                {
                    "id": "3344",
                    "application_id": "7890",
                    "name": "mccoolbotv2",
                    "description": "send a message",
                    "options": [
                        {"type": 3, "name": "message", "description": "send a message"}
                    ],
                },
            ],
        )
    )

    with pytest.raises(DiscordAPIError):
        _get_commands = dispike_object.get_commands()


@respx.mock
def test_get_commands_globally_call_invalid_incoming(dispike_object: Dispike):
    respx.get(f"https://discord.com/api/v8/applications/APPID/commands").mock(
        return_value=Response(
            200,
            json=[
                {
                    "id": "1234",
                    "application_id": "7890",
                    "name": "mccoolbotv1",
                    "options": [
                        {"type": 6, "name": "wave", "description": "wave at a person"}
                    ],
                },
                {
                    "id": "3344",
                    "application_id": "7890",
                    "description": "send a message",
                    "options": [
                        {"type": 3, "name": "message", "description": "send a message"}
                    ],
                },
            ],
        )
    )
    with pytest.raises(ValidationError):
        _get_commands = dispike_object.get_commands()


@respx.mock
def test_get_commands_guild_only_call_successful(dispike_object: Dispike):

    respx.get(
        "https://discord.com/api/v8/applications/APPID/guilds/EXAMPLE_GUILD/commands"
    ).mock(
        return_value=Response(
            200,
            json=[
                {
                    "id": "1234",
                    "application_id": "7890",
                    "name": "mccoolbotv1",
                    "description": "McCoolbot is the coolest bot around.",
                    "options": [
                        {"type": 6, "name": "wave", "description": "wave at a person"}
                    ],
                },
                {
                    "id": "3344",
                    "application_id": "7890",
                    "name": "mccoolbotv2",
                    "description": "send a message",
                    "options": [
                        {"type": 3, "name": "message", "description": "send a message"}
                    ],
                },
            ],
        )
    )
    _get_commands = dispike_object.get_commands(
        guild_only=True, guild_id_passed="EXAMPLE_GUILD"
    )
    for item in _get_commands:
        assert isinstance(item, IncomingApplicationCommand) == True

    assert len(_get_commands) == 2


@respx.mock
def test_get_commands_guild_only_call_fail(dispike_object: Dispike):
    respx.get(
        "https://discord.com/api/v8/applications/APPID/guilds/EXAMPLE_GUILD/commands"
    ).mock(
        return_value=Response(
            404,
            json=[
                {
                    "id": "1234",
                    "application_id": "7890",
                    "name": "mccoolbotv1",
                    "description": "McCoolbot is the coolest bot around.",
                    "options": [
                        {"type": 6, "name": "wave", "description": "wave at a person"}
                    ],
                },
                {
                    "id": "3344",
                    "application_id": "7890",
                    "name": "mccoolbotv2",
                    "description": "send a message",
                    "options": [
                        {"type": 3, "name": "message", "description": "send a message"}
                    ],
                },
            ],
        )
    )
    with pytest.raises(DiscordAPIError):
        _get_commands = dispike_object.get_commands(
            guild_only=True, guild_id_passed="EXAMPLE_GUILD"
        )


@respx.mock
def test_get_commands_guild_only_call_invalid_incoming(dispike_object: Dispike):

    respx.get(
        "https://discord.com/api/v8/applications/APPID/guilds/EXAMPLE_GUILD/commands"
    ).mock(
        return_value=Response(
            200,
            json=[
                {
                    "id": "1234",
                    "application_id": "7890",
                    "name": "mccoolbotv1",
                    "options": [
                        {"type": 6, "name": "wave", "description": "wave at a person"}
                    ],
                },
                {
                    "id": "3344",
                    "application_id": "7890",
                    "description": "send a message",
                    "options": [
                        {"type": 3, "name": "message", "description": "send a message"}
                    ],
                },
            ],
        )
    )
    with pytest.raises(ValidationError):
        _get_commands = dispike_object.get_commands(
            guild_only=True, guild_id_passed="EXAMPLE_GUILD"
        )
