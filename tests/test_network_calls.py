from dispike.register.models.options import (
    CommandChoice,
    CommandOption,
    CommandTypes,
    DiscordCommand,
)
from httpx import Response
from dispike.models.incoming import IncomingApplicationCommand
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


@pytest.fixture
def example_edit_command():
    return DiscordCommand(
        name="exampleCommand",
        description="exampleCommandDescription",
        options=[
            CommandOption(
                name="exampleOption",
                type=CommandTypes.USER,
                description="exampleOptionDescription",
                required=True,
                choices=[CommandChoice(name="test", value="value")],
            )
        ],
    )


@respx.mock
def test_bulk_edit_command_guild_only(
    dispike_object: Dispike, example_edit_command: DiscordCommand
):
    respx.put(
        "https://discord.com/api/v8/applications/APPID/guilds/EXAMPLE_GUILD/commands"
    ).mock(
        return_value=Response(
            200,
            json=[example_edit_command.dict(), example_edit_command.dict()],
        )
    )
    _edit_command = dispike_object.edit_command(
        new_command=[example_edit_command, example_edit_command],
        guild_only=True,
        bulk=True,
        guild_id_passed="EXAMPLE_GUILD",
    )
    assert isinstance(_edit_command, list) == True
    assert len(_edit_command) == 2
    for command in _edit_command:
        assert isinstance(command, DiscordCommand)
        assert command.id == example_edit_command.id
        assert command.name == example_edit_command.name


@respx.mock
def test_bulk_edit_command_globally(
    dispike_object: Dispike, example_edit_command: DiscordCommand
):
    respx.patch("https://discord.com/api/v8/applications/APPID/commands").mock(
        return_value=Response(
            200,
            json=[example_edit_command.dict(), example_edit_command.dict()],
        )
    )
    _edit_command = dispike_object.edit_command(
        new_command=example_edit_command, bulk=True
    )
    assert isinstance(_edit_command, list) == True
    assert len(_edit_command) == 2
    for command in _edit_command:
        assert isinstance(command, DiscordCommand)
        assert command.id == example_edit_command.id
        assert command.name == example_edit_command.name


@respx.mock
def test_single_edit_command_globally(
    dispike_object: Dispike, example_edit_command: DiscordCommand
):
    respx.patch("https://discord.com/api/v8/applications/APPID/commands").mock(
        return_value=Response(
            200,
            json=example_edit_command.dict(),
        )
    )
    _edit_command = dispike_object.edit_command(new_command=example_edit_command)
    assert isinstance(_edit_command, DiscordCommand) == True, type(_edit_command)
    assert _edit_command.id == example_edit_command.id
    assert _edit_command.name == example_edit_command.name


@respx.mock
def test_single_edit_command_guild_only(
    dispike_object: Dispike, example_edit_command: DiscordCommand
):
    respx.patch(
        "https://discord.com/api/v8/applications/APPID/guilds/EXAMPLE_GUILD/commands/1234"
    ).mock(
        return_value=Response(
            200,
            json=example_edit_command.dict(),
        )
    )
    _edit_command = dispike_object.edit_command(
        new_command=example_edit_command,
        command_id=1234,
        guild_only=True,
        guild_id_passed="EXAMPLE_GUILD",
    )
    _edit_command: DiscordCommand
    assert isinstance(_edit_command, DiscordCommand) == True
    assert _edit_command.id == example_edit_command.id
    assert _edit_command.name == example_edit_command.name


@respx.mock
def test_delete_command_guild_only(
    dispike_object: Dispike, example_edit_command: DiscordCommand
):
    respx.delete(
        "https://discord.com/api/v8/applications/APPID/guilds/EXAMPLE_GUILD/commands/1234"
    ).mock(
        return_value=Response(
            204,
            json=example_edit_command.dict(),
        )
    )
    _delete_command = dispike_object.delete_command(
        command_id=1234,
        guild_only=True,
        guild_id_passed="EXAMPLE_GUILD",
    )
    assert _delete_command == True


@respx.mock
def test_failed_delete_command_guild_only(
    dispike_object: Dispike, example_edit_command: DiscordCommand
):
    respx.delete(
        "https://discord.com/api/v8/applications/APPID/guilds/EXAMPLE_GUILD/commands/1234"
    ).mock(
        return_value=Response(
            500,
            json=example_edit_command.dict(),
        )
    )

    with pytest.raises(DiscordAPIError):
        _delete_command = dispike_object.delete_command(
            command_id=1234,
            guild_only=True,
            guild_id_passed="EXAMPLE_GUILD",
        )


@respx.mock
def test_delete_command_globally(
    dispike_object: Dispike,
):
    respx.delete("https://discord.com/api/v8/applications/APPID/commands/1234").mock(
        return_value=Response(
            204,
        )
    )

    _delete_command = dispike_object.delete_command(command_id=1234)
    assert _delete_command == True


@respx.mock
def test_failed_delete_command_globally(
    dispike_object: Dispike,
):
    respx.delete("https://discord.com/api/v8/applications/APPID/commands/1234").mock(
        return_value=Response(
            500,
        )
    )
    with pytest.raises(DiscordAPIError):
        _delete_command = dispike_object.delete_command(command_id=1234)


def test_get_commands_invalid_guild_id_passed(dispike_object: Dispike):
    with pytest.raises(TypeError):
        dispike_object.get_commands(guild_only=True)
