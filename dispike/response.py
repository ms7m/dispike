from .helper.embed import Embed
from .creating.components import ActionRow
import typing
from .errors.network import DiscordAPIError
from .errors.response import ContentIsEmpty, InvalidDiscordResponse
from loguru import logger
import warnings

try:
    from typing import Literal  # pragma: no cover
except ImportError:  # pragma: no cover
    # backport
    from typing_extensions import Literal  # pragma: no cover

if typing.TYPE_CHECKING:
    from .main import Dispike  # pragma: no cover
    from .creating import IncomingDiscordInteraction  # pragma: no cover
    from .creating.allowed_mentions import AllowedMentions  # pragma: no cover


class DiscordResponse(object):
    """Represents an outgoing Discord Response

    Attributes:
        content (str): A plain-text response to a user
        tts (bool): bool returning if the message should be spoken via tts.
        embeds (dict): a List representing .to_dict of an Embed object.
        response (dict): a valid response represented in a dict, to later be converted to JSON.
    """

    def __init__(
        self,
        content: str = None,
        tts: bool = False,
        embeds: typing.List[Embed] = [],
        show_user_input: bool = False,
        follow_up_message=False,
        empherical=False,
        allowed_mentions: "AllowedMentions" = None,
        action_row: ActionRow = None,
        update_message=False,
    ):
        """Initialize a DiscordResponse, you can either pass data into here, or
        simply create a DiscordResponse() and edit via properties.

        Args:
            content (str, optional): A plain-text response to a user
            tts (bool, optional): bool returning if the message should be spoken via tts
            embeds (typing.List[Embed], optional): a List representing .to_dict of an Embed object
            show_user_input (bool, optional): Whether to delete the user's message of calling the command after responding.
            follow_up_message (bool, optional): Whether this is a follow up to a previous message.
            empherical (bool, optional): Whether to send message as an empherical message.
            allowed_mentions (List[AllowedMentions], optional): Let discord filter mentions per configuration.
            update_message (bool, optional): Whether to edit the original message this is responding too.
        """
        if content is not None:
            if not isinstance(content, str):
                raise TypeError(f"Content must be a string")
            elif content == "":
                content = None

        # if isinstance(content, str) == False or content == "" or content != None:
        #    raise TypeError(f"content must be a string. recieved: {content}")

        if not isinstance(tts, bool):
            raise TypeError("tts must be a bool")

        self._content = content
        self._tts = tts
        self._embeds = embeds

        if action_row:
            self._action_row = action_row
        else:
            self._action_row = None

        if show_user_input:
            # show deprecation warning
            warnings.warn(
                "show_user_input is deprecated by Dispike as it is no longer supported by Discord. Future versions of dispike may remove this parameter entirely.",
                DeprecationWarning,
            )  # pragma: no cover
            logger.warning(
                "show_user_input is deprecated by Dispike as it is no longer supported by Discord. Future versions of dispike may remove this parameter entirely."
            )  # pragma: no cover

        self._type_response = 4

        if update_message:
            self._type_response = 7

        self._is_followup = follow_up_message
        self._is_empherical = empherical
        self._allowed_mentions = allowed_mentions

    @property
    def embeds(self) -> typing.List[Embed]:
        """Returns a list of embeds to send to.

        Returns:
            List[Embed]: List of embeds in this object.
        """
        return self._embeds

    @property
    def action_row(self) -> ActionRow:
        """Returns a action row.

        Returns:
            ActionRow: The action row.
        """
        return self._action_row

    def set_type_response(self, type: int):
        self._type_response = type

    def add_new_embed(self, embed_to_add: Embed):
        """Append a new embed, provided with a proper Embed object

        Args:
            embed_to_add (Embed): Proper Embed Object

        Raises:
            TypeError: Raised if you do not pass a proper Embed object.
        """
        if isinstance(embed_to_add, Embed):
            self._embeds.append(embed_to_add)
        else:
            raise TypeError("embed must be a Embed object.")

    @property
    def content(self) -> str:
        """Either set or view the plain-text response to the user.

        Returns:
            str: Content provided
        """
        return self._content

    @content.setter
    def content(self, new_content_string: str):
        self._content = str(new_content_string)

    @property
    def tts(self) -> bool:
        """Either set or view the tts attribute for the user.

        Returns:
            bool: tts
        """
        return self._tts

    @tts.setter
    def tts(self, new_tts: bool):
        self._tts = new_tts

    @property
    def response(self) -> dict:
        """A generated valid discord response

        Returns:
            dict: a valid discord response.
        """

        # Watch this, this may cause an issue.
        self.content = "" if self.content is None else self.content

        if self._is_followup:
            _req = {"content": self.content, "data": {}}

            if self.embeds:
                _req["embeds"] = [x.to_dict() for x in self.embeds]

            if self.tts:
                _req["tts"] = True

            if self._is_empherical:
                logger.info("setting empherical")
                _req["flags"] = 1 << 6

            if self._action_row:
                _req["data"]["components"] = [self.action_row.to_dict()]

            return _req

        _req = {
            "type": self._type_response,
            "data": {
                "tts": self.tts,
                "content": self.content,
                "embeds": [x.to_dict() for x in self.embeds],
            },
        }
        if self._is_empherical:
            _req["data"]["flags"] = 1 << 6

        if self._action_row:
            if self.content == None or self.embeds == [] or self.content == "":
                raise InvalidDiscordResponse(
                    "If creating a response with an action row, content or an embed must be present!"
                )

            _req["data"]["components"] = [self.action_row.to_dict()]

        if self._allowed_mentions:
            _req["allowed_mentions"] = self._allowed_mentions.dict()

        return _req

    def _switch_to_followup_message(self):
        self._is_followup = True

    def __call__(self) -> dict:
        return self.response


class DeferredResponse:
    """Use this class to hint to dispike that the response will be deferred."""

    response = {"type": 5}


class DeferredEmphericalResponse:
    """Use this class to hint to dispike that the response will be deferred and empherical."""

    response = {"type": 5, "data": {"flags": 1 << 6}}


class AcknowledgeComponentResponse:
    """Represents an interaction ACK response"""

    response = {"type": 4, "data": {}}
