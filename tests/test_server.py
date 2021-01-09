from starlette.responses import PlainTextResponse
from dispike.models.incoming import IncomingDiscordInteraction
from dispike.response import DiscordResponse
from fastapi.testclient import TestClient
from dispike.eventer import EventHandler
from dispike import Dispike

from nacl.encoding import HexEncoder
from nacl.signing import SigningKey
import json
import pytest
import typing

from loguru import logger

if typing.TYPE_CHECKING:
    from _pytest.monkeypatch import MonkeyPatch

_generated_signing_key = SigningKey.generate()

_created_timestamp = "1111111"
_created_message = {"id": "1111222", "token": "random_fa", "type": 1, "version": 1}
signed_value = _generated_signing_key.sign(
    f"{_created_timestamp}{json.dumps(_created_message)}".encode(), encoder=HexEncoder
)
verification_key = _generated_signing_key.verify_key.encode(encoder=HexEncoder)


bot = Dispike(
    client_public_key=verification_key.decode(),
    bot_token="NotNeeded",
    application_id="NotNeeded",
)
app = bot.referenced_application
client = TestClient(app)


@app.get("/")
def test_endpoint():
    return {"status": True}


def create_mocked_request(command_name):
    data = {
        "channel_id": "123123",
        "data": {
            "id": "12312312",
            "name": command_name,
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

    class MockState:
        _cached_body = IncomingDiscordInteraction(**data).json().encode()

    class MockResponse:
        state = MockState

    return MockResponse


async def hinted_mock_functions(mocked_events: EventHandler):
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

    @mocked_events.on("hint_return_discord_response")
    async def return_event_hint(*args, **kwargs) -> DiscordResponse:
        logger.info("hint_return_discord_response")
        return DiscordResponse(content="sample")

    @mocked_events.on("hint_return_dict")
    async def return_dict_hint(*args, **kwargs) -> dict:
        logger.info("hint_return_dict")
        return {"sample": "sample"}


async def no_hinted_mocked_functions(mocked_events: EventHandler):
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

    @mocked_events.on("no_hint_return_discord_response")
    async def return_event_no_hinting(*args, **kwargs):
        logger.info("called no_hint_return_discord_response")
        return DiscordResponse(content="sample")

    @mocked_events.on("no_hint_return_dict")
    async def return_event_no_hinting_dict(*args, **kwargs):
        logger.info("no_hint_return_dict")
        return {"sample": "sample"}


@pytest.fixture
@pytest.mark.asyncio
async def mocked_interaction():
    mocked_events = EventHandler()
    await no_hinted_mocked_functions(mocked_events)
    return mocked_events


@pytest.fixture
@pytest.mark.asyncio
async def mocked_interactions_with_hints():
    mocked_events = EventHandler()
    await hinted_mock_functions(mocked_events)
    return mocked_events


def test_ping_endpoint():
    response = client.get("/ping")
    assert response.status_code == 200
    assert (
        response.text
        == "If you see this, Your instance is working and accepting requests."
    )


def test_valid_key_request_redirect():
    response = client.get(
        "/",
        headers={
            "X-Signature-Ed25519": signed_value.signature.decode(),
            "x-Signature-Timestamp": _created_timestamp,
        },
        json=_created_message,
    )
    assert response.status_code == 200


def test_invalid_key_request_redirect():
    response = client.get(
        "/",
        headers={
            "X-Signature-Ed25519": signed_value.signature.decode(),
            "x-Signature-Timestamp": _created_timestamp,
        },
        json={"invalid": "string"},
    )
    assert response.status_code == 401


def test_ack_ping_discord():
    response = client.post(
        "/interactions",
        headers={
            "X-Signature-Ed25519": signed_value.signature.decode(),
            "x-Signature-Timestamp": _created_timestamp,
        },
        json=_created_message,
    )
    assert response.json() == {"type": 1}


@pytest.mark.asyncio
async def test_proper_response_hints_no_hint_return_discord_response(
    mocked_interaction, monkeypatch: "MonkeyPatch"
):
    # we honestly just need a specific attribute from the response..
    from dispike import server

    # monkeypatch.setattr("dispike.server", "EventHandler", mocked_interaction)
    # monkeypatch.setattr("dispike.server", EventHandler, mocked_interaction)

    def return_mocked():
        return mocked_interaction

    monkeypatch.setattr(server, "interaction", mocked_interaction)
    _result = await server.handle_interactions(
        create_mocked_request("no_hint_return_discord_response")
    )
    assert type(_result) == dict
    assert _result["data"]["content"] == "sample"


@pytest.mark.asyncio
async def test_proper_response_hints_no_hint_return_dict(
    mocked_interaction, monkeypatch: "MonkeyPatch"
):
    # we honestly just need a specific attribute from the response..
    from dispike import server

    monkeypatch.setattr(server, "interaction", mocked_interaction)
    _result = await server.handle_interactions(
        create_mocked_request("no_hint_return_dict")
    )
    assert type(_result) == dict
    assert _result == {"sample": "sample"}


@pytest.mark.asyncio
async def test_proper_response_hint_discord_response(
    mocked_interactions_with_hints, monkeypatch: "MonkeyPatch"
):
    # we honestly just need a specific attribute from the response..
    from dispike import server

    monkeypatch.setattr(server, "interaction", mocked_interactions_with_hints)
    monkeypatch.setattr(server, "_RAISE_FOR_TESTING", True)

    _result = await server.handle_interactions(
        create_mocked_request("hint_return_discord_response")
    )
    assert type(_result) == dict
    assert _result["data"]["content"] == "sample"


@pytest.mark.asyncio
async def test_proper_response_hints_hint_return_dict(
    mocked_interactions_with_hints, monkeypatch: "MonkeyPatch"
):
    # we honestly just need a specific attribute from the response..
    from dispike import server

    # monkeypatch.setattr("dispike.server", "EventHandler", mocked_interaction)
    # monkeypatch.setattr("dispike.server", EventHandler, mocked_interaction)

    monkeypatch.setattr(server, "interaction", mocked_interactions_with_hints)
    monkeypatch.setattr(server, "_RAISE_FOR_TESTING", True)
    _result = await server.handle_interactions(
        create_mocked_request("hint_return_dict")
    )
    assert type(_result) == dict
    assert _result == {"sample": "sample"}


@pytest.mark.asyncio
async def test_return_type_5_if_no_event_exists(
    mocked_interactions_with_hints, monkeypatch: "MonkeyPatch"
):
    from dispike import server

    # monkeypatch.setattr("dispike.server", "EventHandler", mocked_interaction)
    # monkeypatch.setattr("dispike.server", EventHandler, mocked_interaction)

    monkeypatch.setattr(server, "interaction", mocked_interactions_with_hints)
    monkeypatch.setattr(server, "_RAISE_FOR_TESTING", True)
    _result = await server.handle_interactions(create_mocked_request("invalid"))
    assert type(_result) == dict
    assert _result == {"type": 5}
