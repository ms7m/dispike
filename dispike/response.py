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
    def __init__(
        self,
        content: str = None,
        tts: bool = False,
        embeds: typing.List[Embed] = [],
        show_user_input: bool = False,
    ):

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
    def embeds(self):
        return self._embeds

    def add_new_embed(self, embed_to_add: Embed):
        if isinstance(embed_to_add, Embed):
            self._embeds.append(embed_to_add.to_dict())
        else:
            raise TypeError("embed must be a Embed object.")

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, new_content_string: str):
        self._content = new_content_string

    @property
    def tts(self):
        return self._tts

    @tts.setter
    def tts(self, new_tts: bool):
        self._tts = new_tts

    @property
    def response(self):
        if self.content == "":
            self.content = None

        return {
            "type": self._type_response,
            "data": {"tts": self.tts, "content": self.content, "embeds": self.embeds},
        }

    def __call__(self):
        return self.response


class NotReadyResponse(object):
    """This is just a representation for a response that is not ready.
    You probably want to use this if you are not ready to immediately return
    a response to an incoming interaction

    You have access to the original arugmnents that arrived with the interaction by accessing
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