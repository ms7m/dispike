from pydantic import BaseModel
from .helper.embed import Embed
import typing
from .errors.network import DiscordAPIError
import httpx
import pickle

try:
    from typing import Literal
except ImportError:
    # backport
    from typing_extensions import Literal

if typing.TYPE_CHECKING:
    from .main import Dispike
    from .models import IncomingDiscordInteraction


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
    ):
        """Initialize a DiscordResponse, you can either pass data into here, or
        simply create a DiscordResponse() and edit via properties.

        Args:
            content (str, optional): A plain-text response to a user
            tts (bool, optional): bool returning if the message should be spoken via tts
            embeds (typing.List[Embed], optional): a List representing .to_dict of an Embed object
            show_user_input (bool, optional): Whether to delete the user's message of calling the command after responding.
        """
        if content != None:
            if isinstance(content, str) == False:
                raise TypeError(f"Content must be a string")
            elif content == "":
                content = None

        # if isinstance(content, str) == False or content == "" or content != None:
        #    raise TypeError(f"content must be a string. recieved: {content}")

        if isinstance(tts, bool) == False:
            raise TypeError("tts must be a bool")

        self._content = content
        self._tts = tts
        self._embeds = [x.to_dict() for x in embeds]
        if show_user_input == False:
            self._type_response = 3
        else:
            self._type_response = 4
        self._is_followup = follow_up_message

    @property
    def embeds(self) -> typing.List[dict]:
        """Returns a list of embeds to send to.

        Returns:
            typing.List[dict]: Embeds represented as a dict.
        """
        # TODO: if accessing .embeds, return an Embed object instead of dict.
        return self._embeds

    def add_new_embed(self, embed_to_add: Embed):
        """Append a new embed, provided with a proper Embed object

        Args:
            embed_to_add (Embed): Proper Embed Object

        Raises:
            TypeError: Raised if you do not pass a proper Embed object.
        """
        if isinstance(embed_to_add, Embed):
            self._embeds.append(embed_to_add.to_dict())
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
        self._content = new_content_string

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
        if self.content == "":
            self.content = None

        if self._is_followup:
            _req = {
                "content": self.content,
            }

            if self.embeds != []:
                _req["embeds"] = self.embeds

            if self.tts == True:
                _req["tts"] = True

            return _req

        return {
            "type": self._type_response,
            "data": {"tts": self.tts, "content": self.content, "embeds": self.embeds},
        }

    def _switch_to_followup_message(self):
        self._is_followup = True

    def __call__(self) -> dict:
        return self.response
