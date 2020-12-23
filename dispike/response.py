from pydantic import BaseModel
from .helper.embed import Embed
import typing

try:
    from typing import Literal
except ImportError:
    # backport
    from typing_extensions import Literal


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
