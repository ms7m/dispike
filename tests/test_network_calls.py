import httpx
from dispike.response import DiscordResponse
from dispike.creating.models.permissions import (
    ApplicationCommandPermissionType,
    ApplicationCommandPermissions,
    GuildApplicationCommandPermissions,
    NewApplicationPermission,
)
from dispike.creating.models.options import (
    CommandChoice,
    CommandOption,
    OptionTypes,
    DiscordCommand,
)
from httpx import Response
from dispike.incoming.incoming_interactions import (
    IncomingApplicationCommand,
    IncomingDiscordInteraction,
)
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
                type=OptionTypes.USER,
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
def test_failed_single_edit_command_guild_only(
    dispike_object: Dispike, example_edit_command: DiscordCommand
):
    respx.patch(
        "https://discord.com/api/v8/applications/APPID/guilds/EXAMPLE_GUILD/commands/1234"
    ).mock(
        return_value=Response(
            401,
            json=example_edit_command.dict(),
        )
    )

    _edit_command = dispike_object.edit_command(
        new_command=example_edit_command,
        command_id=1234,
        guild_only=True,
        guild_id_passed="EXAMPLE_GUILD",
    )
    assert _edit_command == False


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


@respx.mock
def test_set_command_permission(
    dispike_object: Dispike,
):
    respx.put(
        "https://discord.com/api/v8/applications/APPID/guilds/1111/commands/1234/permissions"
    ).mock(
        return_value=Response(
            200,
        )
    )

    _set_commands = dispike_object.set_command_permission(
        command_id=1234,
        guild_id=1111,
        new_permissions=NewApplicationPermission(
            permissions=[
                ApplicationCommandPermissions(
                    permission=True, type=ApplicationCommandPermissionType.ROLE, id=1234
                )
            ]
        ),
    )
    assert _set_commands == True


@respx.mock
def test_failed_set_command_permission(
    dispike_object: Dispike,
):
    respx.put(
        "https://discord.com/api/v8/applications/APPID/guilds/1111/commands/1234/permissions"
    ).mock(
        return_value=Response(
            500,
        )
    )

    _set_commands = dispike_object.set_command_permission(
        command_id=1234,
        guild_id=1111,
        new_permissions=NewApplicationPermission(
            permissions=[
                ApplicationCommandPermissions(
                    permission=True, type=ApplicationCommandPermissionType.ROLE, id=1234
                )
            ]
        ),
    )
    assert _set_commands == False


@respx.mock
@pytest.mark.asyncio
async def test_set_command_permission(
    dispike_object: Dispike,
):
    respx.put(
        "https://discord.com/api/v8/applications/APPID/guilds/1111/commands/1234/permissions"
    ).mock(
        return_value=Response(
            200,
        )
    )

    _set_commands = await dispike_object.async_set_command_permission(
        command_id=1234,
        guild_id=1111,
        new_permissions=NewApplicationPermission(
            permissions=[
                ApplicationCommandPermissions(
                    permission=True, type=ApplicationCommandPermissionType.ROLE, id=1234
                )
            ]
        ),
    )
    assert _set_commands == True


@respx.mock
@pytest.mark.asyncio
async def test_failed_async_set_command_permission(
    dispike_object: Dispike,
):
    respx.put(
        "https://discord.com/api/v8/applications/APPID/guilds/1111/commands/1234/permissions"
    ).mock(
        return_value=Response(
            500,
        )
    )

    _set_commands = await dispike_object.async_set_command_permission(
        command_id=1234,
        guild_id=1111,
        new_permissions=NewApplicationPermission(
            permissions=[
                ApplicationCommandPermissions(
                    permission=True, type=ApplicationCommandPermissionType.ROLE, id=1234
                )
            ]
        ),
    )
    assert _set_commands == False


@respx.mock
@pytest.mark.asyncio
async def test_send_defer_message(
    dispike_object: Dispike,
):
    route = respx.patch(
        "https://discord.com/api/v8/webhooks/APPID/FAKETOKEN/messages/@original",
    ).mock(
        return_value=Response(
            200,
        ),
    )
    _sample_interaction = IncomingDiscordInteraction(
        **{
            "channel_id": "123123",
            "data": {
                "id": "12312312",
                "name": "sample",
                "options": [{"name": "message", "value": "test"}],
            },
            "guild_id": "123123",
            "id": "123123123132",
            "member": {
                "deaf": False,
                "is_pending": False,
                "joined_at": "2019-05-12T18:36:16.878000+00:00",
                "mute": False,
                "nick": None,
                "pending": False,
                "permissions": "2147483647",
                "premium_since": None,
                "roles": [
                    "123123",
                    "123123",
                    "1231233",
                    "1231233133",
                    "12412412414",
                ],
                "user": {
                    "avatar": "b723979992a56",
                    "discriminator": "3333",
                    "id": "234234213122123",
                    "public_flags": 768,
                    "username": "exo",
                },
            },
            "token": "FAKETOKEN",
            "type": 2,
            "version": 1,
        }
    )
    await dispike_object.send_deferred_message(
        original_context=_sample_interaction,
        new_message=DiscordResponse(content="working"),
    )
    assert route.called


@respx.mock
@pytest.mark.asyncio
async def test_send_defer_message_failed(
    dispike_object: Dispike,
):
    route = respx.patch(
        "https://discord.com/api/v8/webhooks/APPID/FAKETOKEN/messages/@original",
    ).mock(
        return_value=Response(
            500,
        ),
    )
    _sample_interaction = IncomingDiscordInteraction(
        **{
            "channel_id": "123123",
            "data": {
                "id": "12312312",
                "name": "sample",
                "options": [{"name": "message", "value": "test"}],
            },
            "guild_id": "123123",
            "id": "123123123132",
            "member": {
                "deaf": False,
                "is_pending": False,
                "joined_at": "2019-05-12T18:36:16.878000+00:00",
                "mute": False,
                "nick": None,
                "pending": False,
                "permissions": "2147483647",
                "premium_since": None,
                "roles": [
                    "123123",
                    "123123",
                    "1231233",
                    "1231233133",
                    "12412412414",
                ],
                "user": {
                    "avatar": "b723979992a56",
                    "discriminator": "3333",
                    "id": "234234213122123",
                    "public_flags": 768,
                    "username": "exo",
                },
            },
            "token": "FAKETOKEN",
            "type": 2,
            "version": 1,
        }
    )
    with pytest.raises(httpx.HTTPError):
        await dispike_object.send_deferred_message(
            original_context=_sample_interaction,
            new_message=DiscordResponse(content="working"),
        )


@respx.mock
@pytest.mark.asyncio
async def test_get_command_permission_for_guild(
    dispike_object: Dispike,
):
    respx.get(
        "https://discord.com/api/v8/applications/APPID/guilds/1111/commands/1234/permissions"
    ).mock(
        return_value=Response(
            200,
            json={
                "id": "1123123123123",
                "application_id": "0000",
                "guild_id": "1111",
                "permissions": [
                    {
                        "id": "1234",
                        "type": 2,
                        "permission": True,
                    }
                ],
            },
        )
    )

    dispike_object._application_id == "0000"
    _get_commands = await dispike_object.async_get_command_permission_in_guild(
        command_id="1234", guild_id=1111
    )
    assert isinstance(_get_commands, GuildApplicationCommandPermissions)
    _get_commands: GuildApplicationCommandPermissions
    assert _get_commands.id == 1123123123123
    assert _get_commands.application_id == 0000
    assert len(_get_commands.permissions) == 1
    assert _get_commands.permissions[0].id == 1234
    assert _get_commands.permissions[0].type == 2
    assert _get_commands.permissions[0].permission == True
    dispike_object._application_id = "APPID"


@respx.mock
def test_sync_get_command_permission_for_guild(
    dispike_object: Dispike,
):
    respx.get(
        "https://discord.com/api/v8/applications/APPID/guilds/1111/commands/1234/permissions"
    ).mock(
        return_value=Response(
            200,
            json={
                "id": "1123123123123",
                "application_id": "0000",
                "guild_id": "1111",
                "permissions": [
                    {
                        "id": "1234",
                        "type": 2,
                        "permission": True,
                    }
                ],
            },
        )
    )

    dispike_object._application_id == "0000"
    _get_commands = dispike_object.get_command_permission_in_guild(
        command_id="1234", guild_id=1111
    )
    assert isinstance(_get_commands, GuildApplicationCommandPermissions)
    _get_commands: GuildApplicationCommandPermissions
    assert _get_commands.id == 1123123123123
    assert _get_commands.application_id == 0000
    assert len(_get_commands.permissions) == 1
    assert _get_commands.permissions[0].id == 1234
    assert _get_commands.permissions[0].type == 2
    assert _get_commands.permissions[0].permission == True
    dispike_object._application_id = "APPID"


@respx.mock
@pytest.mark.asyncio
async def test_failed_get_command_permission_for_guild(
    dispike_object: Dispike,
):
    respx.get(
        "https://discord.com/api/v8/applications/APPID/guilds/1111/commands/1234/permissions"
    ).mock(
        return_value=Response(
            500,
            json={
                "id": "1123123123123",
                "application_id": "0000",
                "guild_id": "1111",
                "permissions": [
                    {
                        "id": "1234",
                        "type": 2,
                        "permission": True,
                    }
                ],
            },
        )
    )

    dispike_object._application_id == "0000"

    with pytest.raises(DiscordAPIError):
        _get_commands = await dispike_object.async_get_command_permission_in_guild(
            command_id="1234", guild_id=1111
        )

    dispike_object._application_id = "APPID"


@respx.mock
def test_sync_failed_get_command_permission_for_guild(
    dispike_object: Dispike,
):
    respx.get(
        "https://discord.com/api/v8/applications/APPID/guilds/1111/commands/1234/permissions"
    ).mock(
        return_value=Response(
            500,
            json={
                "id": "1123123123123",
                "application_id": "0000",
                "guild_id": "1111",
                "permissions": [
                    {
                        "id": "1234",
                        "type": 2,
                        "permission": True,
                    }
                ],
            },
        )
    )

    dispike_object._application_id == "0000"

    with pytest.raises(DiscordAPIError):
        _get_commands = dispike_object.get_command_permission_in_guild(
            command_id="1234", guild_id=1111
        )

    dispike_object._application_id = "APPID"


@respx.mock
@pytest.mark.asyncio
async def test_not_found_get_command_permission_for_guild(
    dispike_object: Dispike,
):
    respx.get(
        "https://discord.com/api/v8/applications/APPID/guilds/1111/commands/1234/permissions"
    ).mock(
        return_value=Response(
            404,
        )
    )

    dispike_object._application_id == "0000"

    _get_commands = await dispike_object.async_get_command_permission_in_guild(
        command_id="1234", guild_id=1111
    )
    assert _get_commands == None

    dispike_object._application_id = "APPID"


@respx.mock
def test_sync_not_found_get_command_permission_for_guild(
    dispike_object: Dispike,
):
    respx.get(
        "https://discord.com/api/v8/applications/APPID/guilds/1111/commands/1234/permissions"
    ).mock(
        return_value=Response(
            404,
        )
    )

    dispike_object._application_id == "0000"

    _get_commands = dispike_object.get_command_permission_in_guild(
        command_id="1234", guild_id=1111
    )
    assert _get_commands == None

    dispike_object._application_id = "APPID"


@respx.mock
@pytest.mark.asyncio
async def test_failed_async_set_command_permission(
    dispike_object: Dispike,
):
    respx.put(
        "https://discord.com/api/v8/applications/APPID/guilds/1111/commands/1234/permissions"
    ).mock(
        return_value=Response(
            500,
        )
    )

    _set_commands = await dispike_object.async_set_command_permission(
        command_id=1234,
        guild_id=1111,
        new_permissions=NewApplicationPermission(
            permissions=[
                ApplicationCommandPermissions(
                    permission=True, type=ApplicationCommandPermissionType.ROLE, id=1234
                )
            ]
        ),
    )
    assert _set_commands == False


#
@respx.mock
@pytest.mark.asyncio
async def test_get_all_command_permission_for_guild(
    dispike_object: Dispike,
):
    respx.get(
        "https://discord.com/api/v8/applications/APPID/guilds/1111/commands/permissions"
    ).mock(
        return_value=Response(
            200,
            json=[
                {
                    "id": "1111",
                    "application_id": "0000",
                    "guild_id": "00",
                    "permissions": [
                        {
                            "id": "1234",
                            "type": 2,
                            "permission": True,
                        }
                    ],
                },
                {
                    "id": "2222",
                    "application_id": "0000",
                    "guild_id": "00",
                    "permissions": [
                        {
                            "id": "1234",
                            "type": 2,
                            "permission": True,
                        }
                    ],
                },
                {
                    "id": "3333",
                    "application_id": "0000",
                    "guild_id": "00",
                    "permissions": [
                        {
                            "id": "1234",
                            "type": 2,
                            "permission": True,
                        }
                    ],
                },
            ],
        )
    )

    dispike_object._application_id == "0000"
    _get_commands = await dispike_object.async_get_all_command_permissions_in_guild(
        guild_id=1111
    )

    assert len(_get_commands) == 3
    for command in _get_commands:
        assert isinstance(command, GuildApplicationCommandPermissions)
        command: GuildApplicationCommandPermissions
        assert command.id in [1111, 2222, 3333]
        assert command.application_id == 0000
        assert len(command.permissions) == 1
        assert command.permissions[0].id == 1234
        assert command.permissions[0].type == 2
        assert command.permissions[0].permission == True

    dispike_object._application_id = "APPID"


@respx.mock
@pytest.mark.asyncio
async def test_failed_get_all_command_permission_for_guild(
    dispike_object: Dispike,
):
    respx.get(
        "https://discord.com/api/v8/applications/APPID/guilds/1111/commands/permissions"
    ).mock(
        return_value=Response(
            500,
            json=[
                {
                    "id": "1111",
                    "application_id": "0000",
                    "guild_id": "1111",
                    "permissions": [
                        {
                            "id": "1234",
                            "type": 2,
                            "permission": True,
                        }
                    ],
                },
                {
                    "id": "2222",
                    "application_id": "0000",
                    "guild_id": "1111",
                    "permissions": [
                        {
                            "id": "1234",
                            "type": 2,
                            "permission": True,
                        }
                    ],
                },
                {
                    "id": "3333",
                    "application_id": "0000",
                    "guild_id": "1111",
                    "permissions": [
                        {
                            "id": "1234",
                            "type": 2,
                            "permission": True,
                        }
                    ],
                },
            ],
        )
    )

    dispike_object._application_id == "0000"

    with pytest.raises(DiscordAPIError):
        _get_commands = await dispike_object.async_get_all_command_permissions_in_guild(
            guild_id=1111
        )

    dispike_object._application_id = "APPID"


@respx.mock
@pytest.mark.asyncio
async def test_no_permissions_get_all_command_permission_for_guild(
    dispike_object: Dispike,
):
    respx.get(
        "https://discord.com/api/v8/applications/APPID/guilds/1111/commands/permissions"
    ).mock(
        return_value=Response(
            200,
            json=[],
        )
    )

    dispike_object._application_id == "0000"
    _get_commands = await dispike_object.async_get_all_command_permissions_in_guild(
        guild_id=1111
    )

    assert len(_get_commands) == 0

    dispike_object._application_id = "APPID"


#
@respx.mock
def test_sync_get_all_command_permission_for_guild(
    dispike_object: Dispike,
):
    respx.get(
        "https://discord.com/api/v8/applications/APPID/guilds/1111/commands/permissions"
    ).mock(
        return_value=Response(
            200,
            json=[
                {
                    "id": "1111",
                    "application_id": "0000",
                    "guild_id": "00",
                    "permissions": [
                        {
                            "id": "1234",
                            "type": 2,
                            "permission": True,
                        }
                    ],
                },
                {
                    "id": "2222",
                    "application_id": "0000",
                    "guild_id": "00",
                    "permissions": [
                        {
                            "id": "1234",
                            "type": 2,
                            "permission": True,
                        }
                    ],
                },
                {
                    "id": "3333",
                    "application_id": "0000",
                    "guild_id": "00",
                    "permissions": [
                        {
                            "id": "1234",
                            "type": 2,
                            "permission": True,
                        }
                    ],
                },
            ],
        )
    )

    dispike_object._application_id == "0000"
    _get_commands = dispike_object.get_all_command_permissions_in_guild(guild_id=1111)

    assert len(_get_commands) == 3
    for command in _get_commands:
        assert isinstance(command, GuildApplicationCommandPermissions)
        command: GuildApplicationCommandPermissions
        assert command.id in [1111, 2222, 3333]
        assert command.application_id == 0000
        assert len(command.permissions) == 1
        assert command.permissions[0].id == 1234
        assert command.permissions[0].type == 2
        assert command.permissions[0].permission == True

    dispike_object._application_id = "APPID"


@respx.mock
def test_sync_failed_get_all_command_permission_for_guild(
    dispike_object: Dispike,
):
    respx.get(
        "https://discord.com/api/v8/applications/APPID/guilds/1111/commands/permissions"
    ).mock(
        return_value=Response(
            500,
            json=[
                {
                    "id": "1111",
                    "application_id": "0000",
                    "guild_id": "1111",
                    "permissions": [
                        {
                            "id": "1234",
                            "type": 2,
                            "permission": True,
                        }
                    ],
                },
                {
                    "id": "2222",
                    "application_id": "0000",
                    "guild_id": "1111",
                    "permissions": [
                        {
                            "id": "1234",
                            "type": 2,
                            "permission": True,
                        }
                    ],
                },
                {
                    "id": "3333",
                    "application_id": "0000",
                    "guild_id": "1111",
                    "permissions": [
                        {
                            "id": "1234",
                            "type": 2,
                            "permission": True,
                        }
                    ],
                },
            ],
        )
    )

    dispike_object._application_id == "0000"

    with pytest.raises(DiscordAPIError):
        _get_commands = dispike_object.get_all_command_permissions_in_guild(
            guild_id=1111
        )

    dispike_object._application_id = "APPID"


@respx.mock
def test_sync_no_permissions_get_all_command_permission_for_guild(
    dispike_object: Dispike,
):
    respx.get(
        "https://discord.com/api/v8/applications/APPID/guilds/1111/commands/permissions"
    ).mock(
        return_value=Response(
            200,
            json=[],
        )
    )

    dispike_object._application_id == "0000"
    _get_commands = dispike_object.get_all_command_permissions_in_guild(guild_id=1111)

    assert len(_get_commands) == 0

    dispike_object._application_id = "APPID"