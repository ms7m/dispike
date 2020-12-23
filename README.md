# dispike

***
an *extremely-extremely* early WIP library for easily creating REST-based webhook bots for discord using the new Slash Commands feature. 

Powered by FastAPI.



## Example

```python

from fastapi import FastAPI
from dispike.server import (
    router,
    interaction,
    DiscordVerificationMiddleware
)
from dispike.models.incoming import IncomingDiscordInteraction # For Type Hinting
from dispike.response import DiscordStringResponse
 

app = FastAPI()
app.add_middleware(DiscordVerificationMiddleware, client_public_key="< Public Key >")
app.include_router(router)



# Now build your bot.


@interaction.on("bot_command_name")
async def handle_command(payload: IncomingDiscordInteraction):
    _response = DiscordStringResponse
    _response.content = f"Hello, {payload.member.user.username}!"
    return _response.response

```
## Result

<p >
  <a href="https://ms7m.me">
    <img
      alt="Website"
      src="./docs/images/demo.png"
    />
  </a>
</p>

## Caveats

- Does not handle registring new commands.
- Does not handle anything other then string responses. (However you are free to return any valid dict in your handler.)
- Not on PyPi
- Does not speak over the discord gateway. You'll need a server to handle requests and responses.
- Python 3.6+