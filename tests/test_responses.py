import json
from dispike.creating.components import (
    Button,
    PartialEmoji,
    ActionRow,
    LinkButton,
    SelectMenu,
)
from dispike.incoming.incoming_interactions import IncomingDiscordInteraction
from dispike.response import DiscordResponse
from dispike.helper.embed import Embed
from .test_dispike import dispike_object
import inspect
import pytest
import typing
import respx
from httpx import Response
from dispike.creating import AllowedMentions, AllowedMentionTypes

if typing.TYPE_CHECKING:
    from dispike import Dispike


@pytest.fixture
def sample_discord_response():
    return DiscordResponse(content="test")


def test_string_response():
    _created_content = DiscordResponse(content="test")
    assert _created_content.content == "test", _created_content.content
    assert (
        _created_content.response["data"]["content"] == "test"
    ), _created_content.content

    _created_content = DiscordResponse(content="test", tts=True)
    assert _created_content.content == "test"
    assert _created_content.tts == True

    _created_content.content = "test2"
    assert _created_content.content == "test2"
    assert _created_content.response["data"]["content"] == "test2"

    _created_content.tts = False
    assert _created_content.tts == False
    assert _created_content.response["data"]["tts"] == False


def test_string_response_with_empherical():
    _created_content = DiscordResponse(content="test", empherical=True)
    assert _created_content.content == "test", _created_content.content
    assert (
        _created_content.response["data"]["content"] == "test"
    ), _created_content.content

    _created_content = DiscordResponse(content="test", tts=True)
    assert _created_content.content == "test"
    assert _created_content.tts == True

    _created_content.content = "test2"
    assert _created_content.content == "test2"
    assert _created_content.response["data"]["content"] == "test2"

    _created_content.tts = False
    assert _created_content.tts == False
    assert _created_content.response["data"]["tts"] == False

    _created_content = DiscordResponse(content="test", empherical=True)
    assert (
        _created_content.response["data"]["flags"] == 1 << 6
    ), _created_content.response


def test_response_with_embed():
    _created_content = DiscordResponse(content="test")
    _created_embed = Embed(title="Test")
    _created_embed.add_field(name="test", value="test")
    _created_content.add_new_embed(_created_embed)

    assert _created_content.embeds[0] == _created_embed


def test_response_with_button():
    _created_button = Button(
        label="test",
        custom_id="test_id",
        disabled=True,
        emoji=PartialEmoji(name="test_emoji", id="123123123132", animated=True),
    )
    _created_link_button = LinkButton(
        label="test", disabled=True, url="https://github.com/"
    )
    _created_content = DiscordResponse(
        content="test",
        action_row=ActionRow(components=[_created_button, _created_link_button]),
    )

    assert _created_content.action_row == ActionRow(
        components=[_created_button, _created_link_button]
    )


def test_response_with_select_menu():
    _created_select_menu = SelectMenu(
        custom_id="test_id",
        disabled=True,
        max_values=1,
        min_values=1,
        options=[
            SelectMenu.SelectMenuOption(
                label="test",
                emoji=PartialEmoji(name="test_emoji", id="123123123132", animated=True),
                description="desc",
                value="test",
                default=True,
            )
        ],
        placeholder="Test",
    )
    _created_content = DiscordResponse(
        content="test", action_row=ActionRow(components=[_created_select_menu])
    )

    assert _created_content.action_row == ActionRow(components=[_created_select_menu])


def test_response_with_allowed_mentions():
    _created_response = DiscordResponse(
        content="test",
        allowed_mentions=AllowedMentions(
            parse=[AllowedMentionTypes.ROLE_MENTIONS], roles=[11111], replied_user=True
        ),
    )
    assert json.loads(json.dumps(_created_response.response))["allowed_mentions"] == {
        "parse": ["roles"],
        "roles": ["11111"],
        "users": [],
        "replied_user": True,
    }
    assert _created_response.response["data"]["content"] == "test"


def test_invalid_embed_object():
    _created_content = DiscordResponse(content="test")
    with pytest.raises(TypeError):
        _created_content.add_new_embed(False)


def test_invalid_content():
    with pytest.raises(TypeError):
        _created_content = DiscordResponse(content=False)

    _created_content = DiscordResponse(content="")
    assert _created_content.content == None

    with pytest.raises(TypeError):
        _created_content = DiscordResponse(content="Test", tts="invalid")


def test_type_response_update():
    _sample = DiscordResponse(content="test")
    _sample.set_type_response = 4
    assert _sample._type_response == 4


def test_type_response_update_message():
    _sample = DiscordResponse(content="test", update_message=True)
    assert _sample._type_response == 7


def test_if_call_function_returns_response():
    _sample = DiscordResponse(content="test")
    assert _sample.__call__() == _sample.response
