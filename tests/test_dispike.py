from dispike import __version__
from dispike import Dispike

import pytest


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

    assert isinstance(dispike_object.interaction, EventHandler) == True, type(
        dispike_object.interaction
    )


def test_valid_shared_client(dispike_object: Dispike):
    from httpx import Client, URL

    assert isinstance(dispike_object.shared_client, Client) == True, type(
        dispike_object.shared_client
    )
    assert dispike_object.shared_client.base_url == URL(
        f"https://discord.com/api/v8/applications/{dispike_object._application_id}/"
    )

def test_reset_registeration(dispike_object: Dispike):
    from nacl.encoding import HexEncoder
    from nacl.signing import SigningKey

    _generated_signing_key = SigningKey.generate()
    verification_key = _generated_signing_key.verify_key.encode(encoder=HexEncoder)

    _current_dispike_object = Dispike(
        client_public_key=verification_key.decode(),
        bot_token="BOTTOKEN",
        application_id="APPID",
    )    

    assert _current_dispike_object.reset_registration(new_bot_token="NewBotToken", new_application_id="newApplicationId") == True
    assert _current_dispike_object._registrator.request_headers != dispike_object._registrator.request_headers
    assert _current_dispike_object._application_id != dispike_object._application_id

def test_invalid_reset_registration(dispike_object: Dispike):
    from nacl.encoding import HexEncoder
    from nacl.signing import SigningKey

    _generated_signing_key = SigningKey.generate()
    verification_key = _generated_signing_key.verify_key.encode(encoder=HexEncoder)

    _current_dispike_object = Dispike(
        client_public_key=verification_key.decode(),
        bot_token="BOTTOKEN",
        application_id="APPID",
    )    

    with pytest.raises(Exception):
        _current_dispike_object.reset_registration(new_bot_token=tuple(0, 0, 0), new_application_id={1: None})


