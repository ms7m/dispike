from dispike import __version__
from dispike import Dispike

import pytest


def test_version():
    assert __version__ == "0.1.0"


def test_initalization():
    from nacl.encoding import HexEncoder
    from nacl.signing import SigningKey

    _generated_signing_key = SigningKey.generate()
    verification_key = _generated_signing_key.verify_key.encode(encoder=HexEncoder)

    assert (
        isinstance(
            Dispike(
                client_public_key=verification_key.decode(),
                bot_token="BOTTOKEN",
                application_id="APPID",
            ),
            Dispike,
        )
        == True
    )


@pytest.fixture
def dispike_object():
    from nacl.encoding import HexEncoder
    from nacl.signing import SigningKey

    _generated_signing_key = SigningKey.generate()
    verification_key = _generated_signing_key.verify_key.encode(encoder=HexEncoder)

    return Dispike(
        client_public_key=verification_key.decode(),
        bot_token="BOTTOKEN",
        application_id="APPID",
    )


def test_valid_fastapi_attribute(dispike_object: Dispike):
    from fastapi import FastAPI

    assert isinstance(dispike_object.referenced_application, FastAPI) == True


def test_valid_registrator_object(dispike_object: Dispike):
    from dispike.register.registrator import RegisterCommands

    assert isinstance(dispike_object._registrator, RegisterCommands)
    assert dispike_object._registrator.register == dispike_object.register


def test_valid_event_handler_object(dispike_object: Dispike):
    from dispike.eventer import EventHandler

    assert isinstance(dispike_object.interaction, EventHandler) == True


def test_valid_shared_client(dispike_object: Dispike):
    from httpx import Client, URL

    assert isinstance(dispike_object.shared_client, Client) == True, type(
        dispike_object.shared_client
    )
    assert dispike_object.shared_client.base_url == URL(
        f"https://discord.com/api/v8/applications/{dispike_object._application_id}/"
    )
