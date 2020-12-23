from dispike.response import DiscordResponse
from dispike.helper.embed import Embed

import pytest


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


def test_response_with_embed():
    _created_content = DiscordResponse(content="test")
    _created_embed = Embed(title="Test")
    _created_embed.add_field(name="test", value="test")
    _created_content.add_new_embed(_created_embed)

    assert isinstance(_created_content.embeds[0], dict) == True
    assert _created_content.embeds[0] != {}


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
