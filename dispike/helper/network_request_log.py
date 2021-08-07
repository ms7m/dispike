from loguru import logger
import httpx


def dispike_httpx_event_hook_outgoing_request(request: httpx.Request):
    logger.log(
        "NETWORK",
        f"Outgoing request <bold yellow>[{request.method}]</bold yellow> <bold white>{request.url}</>: headers: <bold white>{request.headers}</>",
    )


def dispike_httpx_event_hook_incoming_request(response: httpx.Response):
    request = response.request  # type: httpx.Request
    logger.log(
        "NETWORK",
        f"Incoming request: <bold yellow>[{request.method}:{response.status_code}]</bold yellow> <bold white>{request.url}</>: headers: <bold white>{request.headers}</> ",
    )
