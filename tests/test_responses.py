import json
from dispike.errors.network import DiscordAPIError
from dispike.models.incoming import IncomingDiscordInteraction
from dispike.response import DiscordResponse
from dispike.helper.embed import Embed
from .test_dispike import dispike_object
import inspect
import pytest
import typing
import respx
from httpx import Response
from dispike.models.allowed_mentions import AllowedMentions, AllowedMentionTypes

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

    assert isinstance(_created_content.embeds[0], dict) == True
    assert _created_content.embeds[0] != {}


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
