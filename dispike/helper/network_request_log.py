from loguru import logger
import httpx


def dispike_httpx_event_hook_outgoing_request(request: httpx.Request):
    logger.opt(colors=True).log(
        "NETWORK",
        f"Outgoing request <yellow>[{request.method}]</yellow> <white>{request.url}</white>: headers: <white>{request.headers}</white>",
    )


def dispike_httpx_event_hook_incoming_request(response: httpx.Response):
    request = response.request  # type: httpx.Request
    logger.opt(colors=True).log(
        "NETWORK",
        f"Incoming request: <yellow>[{request.method}:{response.status_code}]</yellow> url: <white>{request.url}</white>: headers: <white>{request.headers}</white> ",
    )
