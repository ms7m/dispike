import typing

import httpx
from loguru import logger

from ..response import DiscordResponse
from ..errors.network import DiscordAPIError

if typing.TYPE_CHECKING:
    from ..main import Dispike  # pragma: no cover
    #from ..models import IncomingDiscordInteraction  # pragma: no cover
    from ..incoming import IncomingDiscordSlashInteraction as IncomingDiscordInteraction # pragma: no cover
class FollowUpMessages(object):
    def __init__(
        self,
        bot: "Dispike",
        interaction: "IncomingDiscordInteraction",
    ):
        """A module to handle Follow Up Messages.

        Args:
            bot (Dispike): An already initalized dispike object.
            interaction (IncomingDiscordInteraction): An incoming Discord Interaction
        """
        self._application_id = bot._application_id
        self._interaction_token = interaction.token

        self.base_url = f"https://discord.com/api/v8/webhooks/{self._application_id}/{self._interaction_token}"
        self._async_client = httpx.AsyncClient(base_url=self.base_url)
        self._sync_client = httpx.Client(base_url=self.base_url)

        self._message_id = None

    @logger.catch(reraise=True)
    def create_follow_up_message(self, message: DiscordResponse):
        """Create an initial follow up message. (Sync)

        Args:
            message (DiscordResponse): An already created discord response

        Returns:
            True: If request is successfully made. An exception will rise otherwise

        Raises:
            DiscordAPIError: Discord returning a non-OK status status_code
            TypeError: Invalid type passed.
        """
        if not isinstance(message, DiscordResponse):
            raise TypeError("Message must be a DiscordResponse")

        message._switch_to_followup_message()
        if self._message_id is not None:
            raise TypeError("Creating a followup message can only be done once.")
        try:
            _request = self._sync_client.post(url=self.base_url, json=message.response)
            logger.info("sent request for creation of follow up to discord..")
            if _request.status_code in [200, 201]:
                _parse_request = _request.json()
                self._message_id = _parse_request["id"]
                return True
            else:
                logger.error(
                    f"discord returned a bad status code: {_request.status_code} -> {_request.text} url: {_request.url}"
                )
                raise DiscordAPIError(_request.status_code, _request.text)
        except DiscordAPIError:
            raise

    @logger.catch(reraise=True)
    async def async_create_follow_up_message(self, message: DiscordResponse):
        """Create an initial follow up message. (Async)

        Args:
            message (DiscordResponse): An already created discord response

        Returns:
            True: If request is successfully made. An exception will rise otherwise

        Raises:
            DiscordAPIError: Discord returning a non-OK status status_code
            TypeError: Invalid type passed.
        """
        if not isinstance(message, DiscordResponse):
            raise TypeError("Message must be a DiscordResponse")

        message._switch_to_followup_message()
        if self._message_id is not None:
            raise TypeError("Creating a followup message can only be done once.")
        try:
            _request = await self._async_client.post(
                url=self.base_url, json=message.response
            )
            logger.info("sent request for creation of follow up to discord..")
            if _request.status_code in [200, 201]:
                _parse_request = _request.json()
                self._message_id = _parse_request["id"]
                return True
            else:
                logger.error(
                    f"discord returned a bad status code: {_request.status_code} -> {_request.text} url: {_request.url}"
                )
                raise DiscordAPIError(_request.status_code, _request.text)
        except DiscordAPIError:
            raise

    @logger.catch(reraise=True)
    def edit_follow_up_message(self, updated_message: DiscordResponse):
        """Edit an already sent initial follow-up message. (Sync)

        Args:
            updated_message (DiscordResponse): An already created discord response

        Returns:
            True: If request is successfully made. An exception will rise otherwise

        Raises:
            DiscordAPIError: Discord returning a non-OK status status_code
            TypeError: Invalid type passed.
        """
        if self._message_id is None:
            raise TypeError("a followup message must be sent first!")
        try:
            _request = self._sync_client.patch(
                f"/messages/{self._message_id}", json=updated_message.response
            )
            logger.info(
                f"sent request for edit of follow up to discord [{self._message_id}].."
            )
            if _request.status_code in [200, 201]:
                _parse_request = _request.json()
                self._message_id = _parse_request["id"]
                return True
            else:
                raise DiscordAPIError(_request.status_code, _request.text)
        except DiscordAPIError:
            raise

    @logger.catch(reraise=True)
    async def async_edit_follow_up_message(self, updated_message: DiscordResponse):
        """Edit an already sent initial follow-up message. (Async)

        Args:
            updated_message (DiscordResponse): An already created discord response

        Returns:
            True: If request is successfully made. An exception will rise otherwise

        Raises:
            DiscordAPIError: Discord returning a non-OK status status_code
            TypeError: Invalid type passed.
        """
        if self._message_id is None:
            raise TypeError("a followup message must be sent first!")
        try:
            _request = await self._async_client.patch(
                f"/messages/{self._message_id}", json=updated_message.response
            )
            logger.info(
                f"sent request for edit of follow up to discord [{self._message_id}].."
            )
            if _request.status_code in [200, 201]:
                _parse_request = _request.json()
                self._message_id = _parse_request["id"]
                return True
            else:
                raise DiscordAPIError(_request.status_code, _request.text)
        except DiscordAPIError:
            raise

    @logger.catch(reraise=True)
    def delete_follow_up_message(self):
        """Deletes an already sent initial follow-up message. (sync)

        Returns:
            True: If request is successfully made. An exception will rise otherwise

        Raises:
            DiscordAPIError: Discord returning a non-OK status status_code
            TypeError: Invalid type passed.
        """
        if self._message_id is None:
            raise TypeError("a followup message must be sent first.")
        try:
            _request = self._sync_client.delete(f"/messages/{self._message_id}")
            logger.info(
                f"sent request for deletion of follow up to discord [{self._message_id}].."
            )
            if _request.status_code in [200, 201, 204]:
                self._message_id = None
                return True
            else:
                raise DiscordAPIError(_request.status_code, _request.text)
        except DiscordAPIError:
            raise

    @logger.catch(reraise=True)
    async def async_delete_follow_up_message(self):
        """Deletes an already sent initial follow-up message. (Async)

        Returns:
            True: If request is successfully made. An exception will rise otherwise

        Raises:
            DiscordAPIError: Discord returning a non-OK status status_code
            TypeError: Invalid type passed.
        """
        if self._message_id is None:
            raise TypeError("a followup message must be sent first.")
        try:
            _request = await self._async_client.delete(f"/messages/{self._message_id}")
            logger.info(
                f"sent request for deletion of follow up to discord [{self._message_id}].."
            )
            if _request.status_code in [200, 201, 204]:
                self._message_id = None
                return True
            else:
                raise DiscordAPIError(_request.status_code, _request.text)
        except DiscordAPIError:
            raise
