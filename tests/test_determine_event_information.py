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
    data = {
        "channel_id": "234234234324",
        "data": {
            "id": "12312344231",
            "name": "forex",
            "options": [
                {
                    "name": "latest",
                    "options": [
                        {
                            "name": "convert",
                            "options": [
                                {"name": "symbol_1", "value": "USD"},
                                {"name": "symbol_2", "value": "GBP"},
                            ],
                        }
                    ],
                }
            ],
        },
        "guild_id": "12312123",
        "id": "1234123",
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
                "123123123123123",
                "12312123123123",
                "123123123123123",
                "123123123123123",
                "123123123123123",
            ],
            "user": {
                "avatar": "123123asdfsadfwwqeqwe23123",
                "discriminator": "3333",
                "id": "213123123123",
                "public_flags": 121,
                "username": "aaa",
            },
        },
        "token": "asdfasdf3324",
        "type": 2,
        "version": 1,
    }
    return IncomingDiscordInteraction(**data)


def test_event_information_parse_normal_command(normal_discord_interaction):
    event_name, event_args = determine_event_information(normal_discord_interaction)
    assert event_name == "quote"
    assert event_args == {"worldleader": "exampleValue"}


def test_event_information_parse_subcommand(normal_subcommand_discord_interaction):
    event_name, event_args = determine_event_information(
        normal_subcommand_discord_interaction
    )
    assert event_name == "forex.latest.convert"
    assert event_args == {"symbol_1": "USD", "symbol_2": "GBP"}


def test_invalid_item_raise_error():
    with pytest.raises(TypeError):
        determine_event_information({})


def test_interaction_options_none():
    _sample_incoming_no_options = {
        "channel_id": "1231123123",
        "data": {
            "id": "exampleIDCommand",
            "name": "quote",
            "options": None,
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
    no_options_interaction = IncomingDiscordInteraction(**_sample_incoming_no_options)
    event_name, event_args = determine_event_information(no_options_interaction)
    assert event_name == "quote"
    assert event_args == {}


def test_incoming_discord_object_in_options():
    data = {
        "channel_id": "234234234324",
        "data": {
            "id": "12312344231",
            "name": "forex",
            "options": [
                {
                    "name": "latest",
                    "options": [{"name": "test", "value": "testing"}],
                }
            ],
        },
        "guild_id": "12312123",
        "id": "1234123",
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
                "123123123123123",
                "12312123123123",
                "123123123123123",
                "123123123123123",
                "123123123123123",
            ],
            "user": {
                "avatar": "123123asdfsadfwwqeqwe23123",
                "discriminator": "3333",
                "id": "213123123123",
                "public_flags": 121,
                "username": "aaa",
            },
        },
        "token": "asdfasdf3324",
        "type": 2,
        "version": 1,
    }
    interaction = IncomingDiscordInteraction(**data)
    event_name, event_args = determine_event_information(interaction)
    assert event_name == "forex.latest.test"
    assert event_args == {"test": "testing"}
