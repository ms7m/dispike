from fastapi import FastAPI
from fastapi.testclient import TestClient
from dispike.server import router, DiscordVerificationMiddleware


from nacl.encoding import HexEncoder
from nacl.signing import SigningKey
import json


_generated_signing_key = SigningKey.generate()

_created_timestamp = "1111111"
_created_message = {"id": "1111222", "token": "random_fa", "type": 1, "version": 1}
signed_value = _generated_signing_key.sign(
    f"{_created_timestamp}{json.dumps(_created_message)}".encode(), encoder=HexEncoder
)
verification_key = _generated_signing_key.verify_key.encode(encoder=HexEncoder)

app = FastAPI()
app.add_middleware(
    DiscordVerificationMiddleware, client_public_key=verification_key.decode()
)
app.include_router(router)

client = TestClient(app)


@app.get("/")
def test_endpoint():
    return {"status": True}


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
