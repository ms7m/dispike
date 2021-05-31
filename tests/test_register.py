from httpx import Response
from dispike.register.models import (
    DiscordCommand,
    CommandOption,
    CommandChoice,
    CommandTypes,
)
import pytest
from dispike.errors.network import DiscordAPIError
import respx


@respx.mock
def test_register_command_globally_successful():
    respx.post("https://discord.com/api/v8/applications/EXAMPLE_APP_ID/commands").mock(
        return_value=Response(200)
    )
    from dispike.register.registrator import RegisterCommands

    target_item = RegisterCommands(
        application_id="EXAMPLE_APP_ID", bot_token="EXAMPLE_BOT_TOKEN"
    )
    command_to_be_created = DiscordCommand(
        name="wave",  # this is the main command name.
        description="Send a wave to a nice person! 👋 ",
        options=[
            CommandOption(
                name="person",  # this is the attribute assigned to the value passed.,
                description="person to target",  # this describes the value to pass,
                required=True,
                type=CommandTypes.USER,
            )
        ],
    )
    assert target_item.register(command_to_be_created) == True


@respx.mock
def test_register_command_globally_unsuccessful():
    respx.post("https://discord.com/api/v8/applications/EXAMPLE_APP_ID/commands").mock(
        return_value=Response(404)
    )

    from dispike.register.registrator import RegisterCommands

    target_item = RegisterCommands(
        application_id="EXAMPLE_APP_ID", bot_token="EXAMPLE_BOT_TOKEN"
    )
    command_to_be_created = DiscordCommand(
        name="wave",  # this is the main command name.
        description="Send a wave to a nice person! 👋 ",
        options=[
            CommandOption(
                name="person",  # this is the attribute assigned to the value passed.,
                description="person to target",  # this describes the value to pass,
                required=True,
                type=CommandTypes.USER,
            )
        ],
    )
    with pytest.raises(DiscordAPIError):
        target_item.register(command_to_be_created)


@respx.mock
def test_register_command_guild_only_successful():

    respx.post(
        "https://discord.com/api/v8/applications/EXAMPLE_APP_ID/guilds/EXAMPLE_GUILD/commands"
    ).mock(return_value=Response(200))

    from dispike.register.registrator import RegisterCommands

    target_item = RegisterCommands(
        application_id="EXAMPLE_APP_ID", bot_token="EXAMPLE_BOT_TOKEN"
    )
    command_to_be_created = DiscordCommand(
        name="wave",  # this is the main command name.
        description="Send a wave to a nice person! 👋 ",
        options=[
            CommandOption(
                name="person",  # this is the attribute assigned to the value passed.,
                description="person to target",  # this describes the value to pass,
                required=True,
                type=CommandTypes.USER,
            )
        ],
    )
    assert (
        target_item.register(
            command_to_be_created, guild_only=True, guild_to_target="EXAMPLE_GUILD"
        )
        == True
    )


def test_register_command_guild_only_unsuccessful():
    respx.post(
        "https://discord.com/api/v8/applications/EXAMPLE_APP_ID/guilds/EXAMPLE_GUILD/commands"
    ).mock(return_value=Response(500))

    from dispike.register.registrator import RegisterCommands

    target_item = RegisterCommands(
        application_id="EXAMPLE_APP_ID", bot_token="EXAMPLE_BOT_TOKEN"
    )
    command_to_be_created = DiscordCommand(
        name="wave",  # this is the main command name.
        description="Send a wave to a nice person! 👋 ",
        options=[
            CommandOption(
                name="person",  # this is the attribute assigned to the value passed.,
                description="person to target",  # this describes the value to pass,
                required=True,
                type=CommandTypes.USER,
            )
        ],
    )
    with pytest.raises(DiscordAPIError):
        target_item.register(
            command_to_be_created, guild_only=True, guild_to_target="EXAMPLE_GUILD"
        )


def test_register_command_guild_only_invalid_arguments():
    from dispike.register.registrator import RegisterCommands

    target_item = RegisterCommands(
        application_id="EXAMPLE_APP_ID", bot_token="EXAMPLE_BOT_TOKEN"
    )
    command_to_be_created = DiscordCommand(
        name="wave",  # this is the main command name.
        description="Send a wave to a nice person! 👋 ",
        options=[
            CommandOption(
                name="person",  # this is the attribute assigned to the value passed.,
                description="person to target",  # this describes the value to pass,
                required=True,
                type=CommandTypes.USER,
            )
        ],
    )
    with pytest.raises(TypeError):
        target_item.register(command_to_be_created, guild_only=True)


def test_requests_headers_correct():
    from dispike.register.registrator import RegisterCommands

    target_item = RegisterCommands(
        application_id="EXAMPLE_APP_ID", bot_token="EXAMPLE_BOT_TOKEN"
    )

    assert target_item.request_headers == {"Authorization": f"Bot EXAMPLE_BOT_TOKEN"}


def test_permission_error_for_viewing_bot_token_directly():
    from dispike.register.registrator import RegisterCommands

    target_item = RegisterCommands(
        application_id="EXAMPLE_APP_ID", bot_token="EXAMPLE_BOT_TOKEN"
    )

    with pytest.raises(PermissionError):
        target_item.bot_token


def test_updating_bot_token():
    from dispike.register.registrator import RegisterCommands

    target_item = RegisterCommands(
        application_id="EXAMPLE_APP_ID", bot_token="EXAMPLE_BOT_TOKEN"
    )

    target_item.bot_token = "NEW_BOT_TOKEN"

    assert target_item.request_headers == {"Authorization": "Bot NEW_BOT_TOKEN"}


def test_fail_updating_bot_token_same():
    with pytest.raises(TypeError):
        from dispike.register.registrator import RegisterCommands

        target_item = RegisterCommands(
            application_id="EXAMPLE_APP_ID", bot_token="EXAMPLE_BOT_TOKEN"
        )

        target_item.bot_token = "EXAMPLE_BOT_TOKEN"

        assert target_item.request_headers == {"Authorization": "Bot NEW_BOT_TOKEN"}
