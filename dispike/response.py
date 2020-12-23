
from pydantic import BaseModel
try:
    from typing import Literal
except ImportError:
    # backport
    from typing_extensions import Literal


def DiscordStringResponse(content: str, tts: bool = False, **kwargs):
    return {
        "type": 4,
        "data": {
            "tts": tts,
            "content": content
        }
    }

class DiscordStringResponse(object):
    def __init__(self, content: str = None, tts: bool = False, **kwargs):
        
        
        if isinstance(content, str) == False or content == None or content == "":
            raise TypeError("content must be a string")

        if isinstance(tts, bool) == False:
            raise TypeError("tts must be a bool")

        self._content = content
        self._tts = tts

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
        return {
            "type": 4,
            "data": {
                "tts": self.tts,
                "content": self.content
            }
        }

    def __call__(self):
        return self.response