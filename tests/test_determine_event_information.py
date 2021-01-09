import pytest
from dispike.models import IncomingDiscordInteraction
from dispike.eventer_helpers.determine_event_information import (
    determine_event_information,
)


@pytest.fixture
def normal_discord_interaction():
    _example_response = {
        "channel_id": "1231123123",
        "data": {
            "id": "exampleIDCommand",
            "name": "quote",
            "options": [{"name": "worldleader", "value": "exampleValue"}],
        },
        "guild_id": "123123123",
        "id": "12312123123123",
        "member": {
            "deaf": False,
            "is_pending": False,
            "joined_at": "2021-01-07T15:54:14+0000",
            "mute": False,
            "nick": None,
            "pending": False,
            "permissions": "2147483647",
            "premium_since": None,
            "roles": ["examplerole1"],
            "user": {
                "avatar": "sdfsdfsdfsdf",
                "discriminator": "22212",
                "id": "3333333",
                "public_flags": 768,
                "username": "cooluser",
            },
        },
        "token": "exampleToken",
        "type": 2,
        "version": 1,
    }
    return IncomingDiscordInteraction(**_example_response)


@pytest.fixture
def normal_subcommand_discord_interaction():
    _example_response = {
        "channel_id": "12312312312312",
        "data": {
            "id": "12312312312123",
            "name": "news",
            "options": [
                {"name": "top", "options": [{"name": "country", "value": "fr"}]}
            ],
        },
        "guild_id": "123123123123",
        "id": "12312312123",
        "member": {
            "deaf": False,
            "is_pending": False,
            "joined_at": "2021-01-07T15:54:14+0000",
            "mute": False,
            "nick": None,
            "pending": False,
            "permissions": "2147483647",
            "premium_since": None,
            "roles": [
                "1111",
                "222",
                "333",
                "444",
                "555",
            ],
            "user": {
                "avatar": "asdfasdfasdf",
                "discriminator": "3333",
                "id": "12312323123123",
                "public_flags": 768,
                "username": "cooluser",
            },
        },
        "token": "exampleToken",
        "type": 2,
        "version": 1,
    }
    return IncomingDiscordInteraction(**_example_response)


def test_event_information_parse_normal_command(normal_discord_interaction):
    event_name, event_args = determine_event_information(normal_discord_interaction)
    assert event_name == "quote"
    assert event_args == {"worldleader": "exampleValue"}


def test_event_information_parse_subcommand(normal_subcommand_discord_interaction):
    event_name, event_args = determine_event_information(
        normal_subcommand_discord_interaction
    )
    event_name == "news.top",
    event_args == {"country", "fr"}


def test_invalid_item_raise_error():
    with pytest.raises(TypeError):
        determine_event_information({})