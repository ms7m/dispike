from pydantic import BaseModel
from .helper.embed import Embed
import typing
from .errors.network import DiscordAPIError
import httpx

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

        return {
            "type": self._type_response,
            "data": {"tts": self.tts, "content": self.content, "embeds": self.embeds},
        }

    def __call__(self) -> dict:
        return self.response


class NotReadyResponse(object):
    """This is just a representation for a response that is not ready.
    You probably want to use this if you are not ready to immediately return
    a response to an incoming interaction

    You have access to the original arguments that arrived with the interaction by accessing
    the attribute ``.args``, this returns a dict of kwargs.

    Lower-level access is available by accessing ``._interaction_context``.

    Attributes:
        - sync_send_callback
        - async_send_callback
        - args


    """

    def __init__(
        self, bot: "Dispike", interaction_context: "IncomingDiscordInteraction"
    ):
        """Incoming context to have a response later.

        Args:
            bot (Dispike): Incoming bot object
            interaction_context (IncomingDiscordInteraction): incoming discord interaction
        """
        self._application_id = bot._application_id
        self._interaction_id = interaction_context.id
        self._interaction_token = interaction_context.token

        if len(interaction_context.data.options) > 0:
            self.args = {x.name: x.value for x in interaction_context.data.options}
        else:
            self.args = {}

        self._interaction_context = interaction_context

    def sync_send_callback(self, ready_response: DiscordResponse):
        """Send a callback synchronously

        Args:
            ready_response (DiscordResponse): The DiscordResponse that has been created.

        Raises:
            DiscordAPIError: Any issues that may arrive

        Returns:
            True: if everything works out
        """
        try:
            send_callback = httpx.post(
                f"https://discord.com/api/v8/interactions/{self._interaction_id}/{self._interaction_token}/callback",
                json=ready_response.response,
            )
            if send_callback.status_code not in [200, 201]:
                raise DiscordAPIError(send_callback.status_code, send_callback.text)
            return True
        except Exception:
            raise

    async def async_send_callback(self, ready_response: DiscordResponse):
        """Send a callback asynchronously

        Args:
            ready_response (DiscordResponse): The DiscordResponse that has been created.

        Raises:
            DiscordAPIError: Any issues that may arrive

        Returns:
            True: if everything works out
        """
        try:
            send_callback = await httpx.AsyncClient().post(
                f"https://discord.com/api/v8/interactions/{self._interaction_id}/{self._interaction_token}/callback",
                json=ready_response.response,
            )
            if send_callback.status_code not in [200, 201]:
                raise DiscordAPIError(send_callback.status_code, send_callback.text)
            return True
        except Exception:
            raise