from loguru import logger
from fastapi.responses import JSONResponse, Response
from fastapi import HTTPException
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

import typing

if typing.TYPE_CHECKING:
    from fastapi import FastAPI  # pragma: no cover


class DiscordVerificationMiddleware(BaseHTTPMiddleware):

    """Main middleware for verifying requests are signed by Discord.
    Per documentation.

    You should not need to import this directly.
    """

    def __init__(
        self,
        app: "FastAPI",
        *,
        client_public_key: str,
        testing_skip_verification_of_key: bool = False,
    ):
        """Initialize middleware

        Args:
            app (FastAPI): A valid, initialized FastAPI object
            client_public_key (str): a valid client public key
        """
        super().__init__(app)
        self._client_public_key = client_public_key
        logger.info(f"pub: {self._client_public_key}")
        self._verification_key = VerifyKey(bytes.fromhex(self._client_public_key))
        self._skip_verification_of_key = testing_skip_verification_of_key
        if self._skip_verification_of_key:
            logger.warning(
                "Disabling verification of key on middleware!"
            )  # pragma: no cover

    def verify_request(self, passed_signature: str, timestamp: str, body):
        """Verifies keys.

        Args:
            passed_signature (str): signature provided by discord in headers
            timestamp (str): timestamp provided by discord in headers
            body (TYPE): body provided by discord in headers

        Returns:
            tuple: bool,  status_code
        """

        if self._skip_verification_of_key:
            logger.warning("Verification is disabled! Please re-enable by passing middleware_testing_skip_verification_key_request to False in the main Dispike instance, or set testing_skip_verification_of_key to False.")
            return True, 200

        try:
            message = timestamp.encode() + body
            self._verification_key.verify(message, bytes.fromhex(passed_signature))
            return True, 200
        except BadSignatureError:
            logger.error("bad signature")
            return False, 401
        except Exception:
            logger.exception("exception on verifying request")
            return False, 500

    async def dispatch(
        self,
        request: Request,
        call_next: typing.Callable[[Request], typing.Awaitable[Response]],
    ) -> Response:
        """Intercepts, verifies and dispatches request.

        Args:
            request (Request): Request object
            call_next (typing.Callable[[Request], typing.Awaitable[Response]]): next API endpoint
        """
        logger.debug("intercepting request.")

        if request.url.path == "/ping":
            logger.info("ping, forwarding")
            return await call_next(request)

        try:
            get_signature = request.headers["X-Signature-Ed25519"]
            get_timestamp = request.headers["X-Signature-Timestamp"]

            # https://github.com/encode/starlette/issues/495
            # this is bugged. calling request body will cause a timeout when the next endpoint tries to .body too
            get_body = await request.body()

            # so we need to store the body in the request state.
            request.state._cached_body = get_body
        except Exception:
            # logger.exception("error getting needed data for verification")
            return JSONResponse(
                status_code=400, content={"error_message": "Incorrect request."}
            )

        _status_bool, _status_code = self.verify_request(
            passed_signature=get_signature, timestamp=get_timestamp, body=get_body
        )
        if _status_bool:
            logger.info("approved request. forwarding call")
            _dispatch_request = await call_next(request)
            return _dispatch_request

        return JSONResponse(status_code=_status_code)
