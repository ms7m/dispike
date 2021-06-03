from dispike.models.incoming import IncomingButtonInteraction
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
def button_interaction_raw():
    data = {
        "version": 1,
        "type": 3,
        "token": "unique_interaction_token",
        "message": {
            "type": 0,
            "tts": False,
            "timestamp": "2021-05-19T02:12:51.710000+00:00",
            "pinned": False,
            "mentions": [],
            "mention_roles": [],
            "mention_everyone": False,
            "id": "844397162624450620",
            "flags": 0,
            "embeds": [],
            "edited_timestamp": None,
            "content": "This is a message with components.",
            "components": [
                {
                    "type": 1,
                    "components": [
                        {
                            "type": 2,
                            "label": "Click me!",
                            "style": 1,
                            "custom_id": "click_one",
                        }
                    ],
                }
            ],
            "channel_id": "345626669114982402",
            "author": {
                "username": "Mason",
                "public_flags": 131141,
                "id": "53908232506183680",
                "discriminator": "1337",
                "avatar": "a_d5efa99b3eeaa7dd43acca82f5692432",
            },
            "attachments": [],
        },
        "member": {
            "user": {
                "username": "Mason",
                "public_flags": 131141,
                "id": "53908232506183680",
                "discriminator": "1337",
                "avatar": "a_d5efa99b3eeaa7dd43acca82f5692432",
            },
            "roles": ["290926798626357999"],
            "premium_since": None,
            "permissions": "17179869183",
            "pending": False,
            "nick": None,
            "mute": False,
            "joined_at": "2017-03-13T19:19:14.040000+00:00",
            "is_pending": False,
            "deaf": False,
            "avatar": None,
        },
        "id": "846462639134605312",
        "guild_id": "290926798626357999",
        "data": {"custom_id": "click_one", "component_type": 2},
        "channel_id": "345626669114982999",
        "application_id": "290926444748734465",
    }
    return data


@pytest.fixture
def button_interaction(button_interaction_raw):
    return IncomingButtonInteraction(**button_interaction_raw)


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


def test_incoming_button_interaction(button_interaction_raw):
    assert isinstance(
        IncomingButtonInteraction(**button_interaction_raw),
        IncomingButtonInteraction,
    ), "Unable to convert to button interaction."


def test_event_information_button_interaction(button_interaction):
    assert determine_event_information(button_interaction) == "button.click_one"


def test_invalid_item_raise_error():
    with pytest.raises(TypeError):
        determine_event_information({})