from dispike.models.allowed_mentions import AllowedMentions, AllowedMentionTypes
from dispike.response import DiscordResponse
import json


def test_creation_of_allowed_mentions_users():
    _create_allowed_mentions = AllowedMentions(
        parse=[AllowedMentionTypes.USER_MENTIONS], users=["11111"], replied_user=True
    )
    assert json.loads(_create_allowed_mentions.json()) == {
        "parse": ["users"],
        "users": ["11111"],
        "roles": [],
        "replied_user": True,
    }


def test_creation_of_allowed_mentions_roles():
    _create_allowed_mentions = AllowedMentions(
        parse=[AllowedMentionTypes.ROLE_MENTIONS], roles=["11111"], replied_user=True
    )
    assert json.loads(_create_allowed_mentions.json()) == {
        "parse": ["roles"],
        "users": [],
        "roles": ["11111"],
        "replied_user": True,
    }


def test_creation_of_allowed_mentions_everyone():
    _create_allowed_mentions = AllowedMentions(
        parse=[AllowedMentionTypes.EVERYONE_MENTIONS], replied_user=True
    )
    assert json.loads(_create_allowed_mentions.json()) == {
        "parse": ["everyone"],
        "users": [],
        "roles": [],
        "replied_user": True,
    }