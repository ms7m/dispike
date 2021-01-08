import typing

import httpx
from loguru import logger

from ..response import DiscordResponse
from ..errors.network import DiscordAPIError

if typing.TYPE_CHECKING:
    from ..main import Dispike
    from ..models import IncomingDiscordInteraction


class FollowUpMessages(object):
    def __init__(
        self,
        bot: "Dispike",
        interaction: "IncomingDiscordInteraction",
        storage_adapter=None,
    ):

        self._application_id = bot._application_id
        self._interaction_token = interaction.token
        self._storage_adapter = storage_adapter

        self.base_url = f"https://discord.com/api/v8/webhooks/{self._application_id}/{self._interaction_token}"
        self._async_client = httpx.AsyncClient(base_url=self.base_url)
        self._sync_client = httpx.Client(base_url=self.base_url)

        self._message_id = None

    def create_follow_up_message(self, message: DiscordResponse):
        if self._message_id != None:
            raise TypeError("Creating a followup message can only be done once.")
        try:
            _request = self._sync_client.post("/", json=message.response)
            if _request.status_code in [200, 201]:
                _parse_request = _request.json()
                self._message_id = _parse_request["id"]
                return True
            else:
                raise DiscordAPIError(_request.status_code, _request.text)
        except DiscordAPIError:
            raise
        except Exception:
            logger.exception("error creating message.")
            raise

    async def async_create_follow_up_message(self, message: DiscordResponse):
        if self._message_id != None:
            raise TypeError("Creating a followup message can only be done once.")
        try:
            _request = await self._async_client.post("/", json=message.response)
            if _request.status_code in [200, 201]:
                _parse_request = _request.json()
                self._message_id = _parse_request["id"]
                return True
            else:
                raise DiscordAPIError(_request.status_code, _request.text)
        except DiscordAPIError:
            raise
        except Exception:
            logger.exception("error creating message.")
            raise

    def edit_follow_up_message(self, updated_message: DiscordResponse):
        if self._message_id == None:
            raise TypeError("a followup message must be sent first!")
        try:
            _request = self._sync_client.patch(
                f"/messages/{self._message_id}", json=updated_message.response
            )
            if _request.status_code in [200, 201]:
                _parse_request = _request.json()
                self._message_id = _parse_request["id"]
                return True
            else:
                raise DiscordAPIError(_request.status_code, _request.text)
        except DiscordAPIError:
            raise
        except Exception:
            logger.exception("error creating message.")
            raise

    async def async_edit_follow_up_message(self, updated_message: DiscordResponse):
        if self._message_id == None:
            raise TypeError("a followup message must be sent first!")
        try:
            _request = await self._async_client.patch(
                f"/messages/{self._message_id}", json=updated_message.response
            )
            if _request.status_code in [200, 201]:
                _parse_request = _request.json()
                self._message_id = _parse_request["id"]
                return True
            else:
                raise DiscordAPIError(_request.status_code, _request.text)
        except DiscordAPIError:
            raise
        except Exception:
            logger.exception("error creating message.")
            raise

    def delete_follow_up_message(self):
        if self._message_id == None:
            raise TypeError("a followup message must be sent first.")
        try:
            _request = self._sync_client.delete(f"/messages/{self._message_id}")
            if _request.status_code in [200, 201]:
                _parse_request = _request.json()
                self._message_id = _parse_request["id"]
                return True
            else:
                raise DiscordAPIError(_request.status_code, _request.text)
        except DiscordAPIError:
            raise
        except Exception:
            logger.exception("error creating message.")
            raise

    async def async_delete_follow_up_message(self):
        if self._message_id == None:
            raise TypeError("a followup message must be sent first.")
        try:
            _request = await self._sync_client.delete(f"/messages/{self._message_id}")
            if _request.status_code in [200, 201]:
                _parse_request = _request.json()
                self._message_id = _parse_request["id"]
                return True
            else:
                raise DiscordAPIError(_request.status_code, _request.text)
        except DiscordAPIError:
            raise
        except Exception:
            logger.exception("error creating message.")
            raise