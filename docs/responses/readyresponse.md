## Ready Response

An order to properly return a valid response, you will need to use the ``DiscordResponse`` object. 

```python
from dispike.responses import DiscordResponse
```

``content``, ``embeds``, and ``tts`` is not required immediately, and can be configured later..

However, settings such as ``show_user_input`` and ``folow_up_message`` are set at first initalization and cannot be changed.  


```python
from dispike.responses import DiscordResponse

response = DiscordResponse()
response.content = "Content Text Here"
```

```python
from dispike.responses import DiscordResponse
from dispike.helper import Embed
async def sample_function(...) -> DiscordResponse:
    ...
    return DiscordResponse(
        content="Content Text Here",
        tts=False,
        embeds=[Embed(...), Embed(...)],
        show_user_input=True
    )
```


???+ info
    DiscordResponse is simply a helper to help you generate valid response to discord. If you are able to generate a valid response yourself, you can simply type-hint your function to hint at a dict and return a *proper* response. This is only recommended for **Advanced** users.

:::dispike.response.DiscordResponse