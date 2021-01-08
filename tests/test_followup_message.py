import pytest
import respx
from dispike.followup import FollowUpMessages
from httpx import Response
import typing

if typing.TYPE_CHECKING:
    from dispike import Dispike
    from dispike.models.incoming import (
        IncomingApplicationCommand,
        IncomingDiscordInteraction,
    )


@pytest.fixture
def return_token():
    return {"token": "exampleToken", "id": "exampleId"}


@pytest.fixture
def dispike_object():
    from dispike import Dispike

    from nacl.encoding import HexEncoder
    from nacl.signing import SigningKey

    _generated_signing_key = SigningKey.generate()
    verification_key = _generated_signing_key.verify_key.encode(encoder=HexEncoder)

    return Dispike(
        client_public_key=verification_key.decode(),
        bot_token="BOTTOKEN",
        application_id="APPID",
    )


@pytest.fixture
def example_incoming_response():
    from dispike.models.incoming import IncomingDiscordInteraction

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
                "username": "exo",
            },
        },
        "token": "exampleToken",
        "type": 2,
        "version": 1,
    }

    return IncomingDiscordInteraction(**_example_response)


@pytest.fixture
def followup_message_object(dispike_object: "Dispike", example_incoming_response):
    return FollowUpMessages(bot=dispike_object, interaction=example_incoming_response)


@pytest.fixture
def create_example_response():
    from dispike.response import DiscordResponse

    return DiscordResponse(content="not needed.")


def test_initalization_of_object(
    dispike_object: "Dispike", example_incoming_response: "IncomingDiscordInteraction"
):
    _create_object = FollowUpMessages(dispike_object, example_incoming_response)
    assert _create_object._application_id == "APPID"
    assert _create_object._interaction_token == "exampleToken"


@respx.mock
def test_mock_create_followup_message_sync(
    followup_message_object: FollowUpMessages, create_example_response
):
    respx.post(
        f"https://discord.com/api/v8/webhooks/{followup_message_object._application_id}/{followup_message_object._interaction_token}/"
    ).mock(return_value=Response(200, json={"id": "exampleIncomingToken"}))

    assert (
        followup_message_object.create_follow_up_message(
            message=create_example_response
        )
        == True
    )


@respx.mock
@pytest.mark.asyncio
async def test_mock_create_followup_message_async(
    followup_message_object: FollowUpMessages, create_example_response
):
    respx.post(
        f"https://discord.com/api/v8/webhooks/{followup_message_object._application_id}/{followup_message_object._interaction_token}/"
    ).mock(return_value=Response(200, json={"id": "exampleIncomingToken"}))

    assert (
        await followup_message_object.async_create_follow_up_message(
            message=create_example_response
        )
        == True
    )