from dispike.incoming.discord_types.role import Role
from dispike.incoming.discord_types.member import PartialMember
from dispike.incoming.discord_types.channel import PartialChannel
from dispike.incoming import *
import pytest

from dispike.incoming.incoming_interactions import (
    IncomingDiscordButtonInteraction,
    IncomingDiscordSelectMenuInteraction,
)



@pytest.fixture
def incoming_resolved_interaction():
    return IncomingDiscordSlashInteraction(**{
    "application_id": "781316040038023198",
    "channel_id": "781315923503611944",
    "data": {
        "id": "873464975270760449",
        "name": "latestdebug",
        "options": [
            {"name": "member_one", "type": 9, "value": "781316040038023198"},
            {"name": "member_two", "type": 9, "value": "356139270446120960"},
            {"name": "channel_one", "type": 7, "value": "781315923503611944"},
            {"name": "channel_two", "type": 7, "value": "670059293105586226"},
            {"name": "role_one", "type": 8, "value": "577224182014672906"},
            {"name": "role_two", "type": 8, "value": "577224126184292352"},
        ],
        "resolved": {
            "channels": {
                "670059293105586226": {
                    "id": "670059293105586226",
                    "name": "bot-cmds",
                    "parent_id": "576970477306773545",
                    "permissions": "274877906943",
                    "type": 0,
                },
                "781315923503611944": {
                    "id": "781315923503611944",
                    "name": "bot-talking",
                    "parent_id": "576970477306773545",
                    "permissions": "274877906943",
                    "type": 0,
                },
            },
            "members": {
                "356139270446120960": {
                    "avatar": None,
                    "is_pending": False,
                    "joined_at": "2019-05-12T18:36:16.878000+00:00",
                    "nick": None,
                    "pending": False,
                    "permissions": "274877906943",
                    "premium_since": None,
                    "roles": [
                        "715808753273929728",
                        "577200612618403875",
                        "577200590803697676",
                        "681590545952407637",
                        "741507081403629659",
                    ],
                },
                "781316040038023198": {
                    "avatar": None,
                    "is_pending": False,
                    "joined_at": "2020-11-26T00:33:21.321000+00:00",
                    "nick": None,
                    "pending": False,
                    "permissions": "247064809024",
                    "premium_since": None,
                    "roles": ["781316707754704947", "781316631997054999"],
                },
            },
            "roles": {
                "577224126184292352": {
                    "color": 3092790,
                    "hoist": False,
                    "id": "577224126184292352",
                    "managed": False,
                    "mentionable": False,
                    "name": "---- Legit Roles -----",
                    "permissions": "6546775616",
                    "position": 27,
                },
                "577224182014672906": {
                    "color": 3092790,
                    "hoist": False,
                    "id": "577224182014672906",
                    "managed": False,
                    "mentionable": False,
                    "name": "---- Joke Roles  -----",
                    "permissions": "6546775616",
                    "position": 23,
                },
            },
            "users": {
                "356139270446120960": {
                    "avatar": "6419d97dc9bb653f80a7d386882207cb",
                    "discriminator": "3333",
                    "id": "356139270446120960",
                    "public_flags": 768,
                    "username": "exo",
                },
                "781316040038023198": {
                    "avatar": "48efd456ffdb018f9c3d799326c7ee2c",
                    "bot": True,
                    "discriminator": "6689",
                    "id": "781316040038023198",
                    "public_flags": 0,
                    "username": "Completely Normal Female",
                },
            },
        },
        "type": 1,
    },
    "guild_id": "576970476715507729",
    "id": "873470527946260480",
    "member": {
        "avatar": None,
        "deaf": False,
        "is_pending": False,
        "joined_at": "2019-05-12T18:36:16.878000+00:00",
        "mute": False,
        "nick": None,
        "pending": False,
        "permissions": "274877906943",
        "premium_since": None,
        "roles": [
            "715808753273929728",
            "577200612618403875",
            "577200590803697676",
            "681590545952407637",
            "741507081403629659",
        ],
        "user": {
            "avatar": "6419d97dc9bb653f80a7d386882207cb",
            "discriminator": "3333",
            "id": "356139270446120960",
            "public_flags": 768,
            "username": "exo",
        },
    },
    "token": "aW50ZXJhY3Rpb246ODczNDcwNTI3OTQ2MjYwNDgwOjh4QzQ0MW5hUWVCSWNkallWQVJ6dXNUMUx0eVM5QjZuQ01XTlZyT0dUeDFMTWtZU1ZNYW5rcjRjZGZsNjBNWng2eGZCdmxTQUI0d0hJQkp2cURxUU9IS2tPdmdTcm5mSHNZdUZNSXlGS1pIa2RCS1Y5ejg4OEtUUW9ac1U5UHR1",
    "type": 2,
    "version": 1,
})
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
    _create_model = IncomingDiscordSlashInteraction(**data)
    assert len(_create_model.data.options) == 1


def test_valid_incoming_button():
    data = {
        "channel_id": "123123",
        "data": {"custom_id": "click_one", "component_type": 2},
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
        "type": 3,
        "version": 1,
    }

    _create_model = IncomingDiscordButtonInteraction(**data)
    assert _create_model.data.custom_id == "click_one"


def test_valid_incoming_select_menu():
    data = {
        "channel_id": "123123",
        "data": {
            "component_type": 3,
            "custom_id": "class_select_1",
            "values": ["mage", "rogue"],
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
        "type": 3,
        "version": 1,
    }

    _create_model = IncomingDiscordSelectMenuInteraction(**data)
    assert _create_model.data.custom_id == "class_select_1"
    assert _create_model.data.values == ["mage", "rogue"]


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
    _create_model = IncomingDiscordSlashInteraction(**data)
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
    _created_object = IncomingDiscordSlashInteraction(**data)
    assert _created_object.data.name == "sendmessage"

def test_lookup_user_resolved_function(incoming_resolved_interaction: IncomingDiscordSlashInteraction):
    from dispike.incoming.attribute_helpers.resolved_interactions import lookup_resolved_user_helper
    
    assert isinstance(lookup_resolved_user_helper(incoming_resolved_interaction, "356139270446120960"), User)
    assert lookup_resolved_user_helper(incoming_resolved_interaction, "356139270446120960").id == 356139270446120960
    assert lookup_resolved_user_helper(incoming_resolved_interaction, "356139270446120960").public_flags == 768
    assert lookup_resolved_user_helper(incoming_resolved_interaction, "356139270446120960").username == "exo"
    assert lookup_resolved_user_helper(incoming_resolved_interaction, "356139270446120960").discriminator == "3333"
    assert lookup_resolved_user_helper(incoming_resolved_interaction, "bad") == None


def test_lookup_members_resolved_function(incoming_resolved_interaction: IncomingDiscordSlashInteraction):
    from dispike.incoming.attribute_helpers.resolved_interactions import lookup_resolved_member_helper
    
    assert isinstance(lookup_resolved_member_helper(incoming_resolved_interaction, "356139270446120960"), PartialMember)
    assert lookup_resolved_member_helper(incoming_resolved_interaction, "bad") == None


def test_lookup_roles_resolved_function(incoming_resolved_interaction: IncomingDiscordSlashInteraction):
    from dispike.incoming.attribute_helpers.resolved_interactions import lookup_resolved_role_helper
    
    assert isinstance(lookup_resolved_role_helper(incoming_resolved_interaction, "577224126184292352"), Role)
    assert lookup_resolved_role_helper(incoming_resolved_interaction, "bad") == None

def test_lookup_channels_resolved_function(incoming_resolved_interaction: IncomingDiscordSlashInteraction):
    from dispike.incoming.attribute_helpers.resolved_interactions import lookup_resolved_channel_helper
    
    assert isinstance(lookup_resolved_channel_helper(incoming_resolved_interaction, "670059293105586226"), PartialChannel)
    assert lookup_resolved_channel_helper(incoming_resolved_interaction, "bad") == None


    