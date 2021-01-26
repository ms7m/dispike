## Ready Response

The ``DiscordResponse`` is available as a convienence object to assist you in generating a proper payload to return to discord. 

Some methods and functions may require you to *only* use a valid ``DiscordResponse``. 

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


### Empherical Messages
Empherical messages (messages/responses that are only visible to the person who sent them ) are available by setting the optional ``empherical`` parameter to ``True``. 

???+ info
    Setting a response to be empherical *after* initalization can be done by setting the ``._is_empherical`` attribute. (Note this will be changed in newer versions of Dispike.)

```python
from dispike.responses import DiscordResponse

response = DiscordResponse(empherical=True)
response.content = "Content Text Here"
```

???+ info
    DiscordResponse is simply a helper to help you generate valid response to discord. If you are able to generate a valid response yourself, you can simply type-hint your function to hint at a dict and return a *proper* response. This is only recommended for **Advanced** users.

:::dispike.response.DiscordResponse