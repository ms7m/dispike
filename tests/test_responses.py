
from dispike.response import DiscordStringResponse

import pytest

def test_string_response():
    _created_content = DiscordStringResponse(content="test")
    assert _created_content.content == "test", _created_content.content
    assert _created_content.response['data']['content'] == "test", _created_content.content

    _created_content = DiscordStringResponse(content="test", tts=True)
    assert _created_content.content == "test"
    assert _created_content.tts == True

    _created_content.content = "test2"
    assert _created_content.content == "test2"
    assert _created_content.response['data']['content'] == "test2"


    _created_content.tts = False
    assert _created_content.tts == False
    assert _created_content.response['data']['tts'] == False

def test_invalid_content():
    with pytest.raises(TypeError):
        _created_content = DiscordStringResponse(content=False)

    with pytest.raises(TypeError):
        _created_content = DiscordStringResponse(content=None)

    with pytest.raises(TypeError):
        _created_content = DiscordStringResponse(content='')  

    with pytest.raises(TypeError):
        _created_content = DiscordStringResponse(content="Test", tts="invalid")
        
     