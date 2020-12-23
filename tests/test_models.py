from dispike.models import *
import pytest


def test_valid_incoming_one_option():
    data = {
        "channel_id": "123123",
        "data": {
            "id": "12312312",
            "name": "sendmessage",
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
        "token": "Null",
        "type": 2,
        "version": 1,
    }
    _create_model = IncomingDiscordInteraction(**data)
    assert len(_create_model.data.options) == 1


def test_valid_incoming_multiple_options():
    data = {
        "channel_id": "123123",
        "data": {
            "id": "12312312",
            "name": "sendmessage",
            "options": [
                {"name": "message", "value": "test"},
                {"name": "message2", "value": "test2"},
            ],
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
        "token": "Null",
        "type": 2,
        "version": 1,
    }
    _create_model = IncomingDiscordInteraction(**data)
    assert len(_create_model.data.options) == 2


def test_valid_interaction_name():
    data = {
        "channel_id": "123123",
        "data": {
            "id": "12312312",
            "name": "sendmessage",
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
        "token": "Null",
        "type": 2,
        "version": 1,
    }
    _created_object = IncomingDiscordInteraction(**data)
    assert _created_object.data.name == "sendmessage"
