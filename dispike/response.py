
from pydantic import BaseModel
try:
    from typing import Literal
except ImportError:
    # backport
    from typing_extensions import Literal

class DiscordStringResponse(object):
    def __init__(self, content: str = "Default String", tts: bool = False, **kwargs):
        
        if isinstance(content, str) == False or content == "":
            raise TypeError(f"content must be a string. recieved: {content}")

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
        if self.content == None:
            raise TypeError("Content cannot be empty.")

        return {
            "type": 4,
            "data": {
                "tts": self.tts,
                "content": self.content
            }
        }

    def __call__(self):
        return self.response