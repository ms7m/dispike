from dispike.errors.network import DiscordAPIError
from dispike.models.incoming import IncomingDiscordInteraction
from dispike.response import DiscordResponse, NotReadyResponse
from dispike.helper.embed import Embed
from .test_dispike import dispike_object
import inspect
import pytest
import typing
import respx
from httpx import Response

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


@pytest.mark.asyncio
def test_not_ready_response(dispike_object: "Dispike"):
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

    sample_interaction = IncomingDiscordInteraction(**data)
    _created_content = NotReadyResponse(
        bot=dispike_object, interaction_context=sample_interaction
    )

    assert _created_content._application_id == dispike_object._application_id
    assert _created_content._interaction_id == 123123123132
    assert _created_content._interaction_token == "Null"
    assert _created_content.args == {"message": "test"}

    assert (
        inspect.iscoroutinefunction(_created_content.async_send_callback) == True
    ), type(_created_content.async_send_callback)
    assert inspect.ismethod(_created_content.sync_send_callback) == True, type(
        _created_content.sync_send_callback
    )


@respx.mock
@pytest.mark.asyncio
async def test_async_send_callback_for_not_ready(
    dispike_object: "Dispike", sample_discord_response
):
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

    sample_interaction = IncomingDiscordInteraction(**data)
    _created_content = NotReadyResponse(
        bot=dispike_object, interaction_context=sample_interaction
    )

    # TODO: Make a file full of common pytest fixtures for easy access.
    respx.post(
        f"https://discord.com/api/v8/interactions/{_created_content._interaction_id}/{_created_content._interaction_token}/callback"
    ).mock(return_value=Response(status_code=200))

    await _created_content.async_send_callback(sample_discord_response)


@respx.mock
@pytest.mark.asyncio
async def test_async_send_callback_for_not_ready_invalid_response(
    dispike_object: "Dispike", sample_discord_response
):
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

    sample_interaction = IncomingDiscordInteraction(**data)
    _created_content = NotReadyResponse(
        bot=dispike_object, interaction_context=sample_interaction
    )

    respx.post(
        f"https://discord.com/api/v8/interactions/{_created_content._interaction_id}/{_created_content._interaction_token}/callback"
    ).mock(return_value=Response(status_code=500))

    with pytest.raises(DiscordAPIError):
        await _created_content.async_send_callback(sample_discord_response)


@respx.mock
def test_sync_send_callback_for_not_ready(
    dispike_object: "Dispike", sample_discord_response
):
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

    sample_interaction = IncomingDiscordInteraction(**data)
    _created_content = NotReadyResponse(
        bot=dispike_object, interaction_context=sample_interaction
    )

    # TODO: Make a file full of common pytest fixtures for easy access.
    respx.post(
        f"https://discord.com/api/v8/interactions/{_created_content._interaction_id}/{_created_content._interaction_token}/callback"
    ).mock(return_value=Response(status_code=200))

    assert _created_content.sync_send_callback(sample_discord_response) == True


@respx.mock
def test_sync_send_callback_for_not_ready_invalid_response(
    dispike_object: "Dispike", sample_discord_response
):
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

    sample_interaction = IncomingDiscordInteraction(**data)
    _created_content = NotReadyResponse(
        bot=dispike_object, interaction_context=sample_interaction
    )

    respx.post(
        f"https://discord.com/api/v8/interactions/{_created_content._interaction_id}/{_created_content._interaction_token}/callback"
    ).mock(return_value=Response(status_code=500))

    with pytest.raises(DiscordAPIError):
        _created_content.sync_send_callback(sample_discord_response)