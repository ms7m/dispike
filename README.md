# dispike

***
an *extremely-extremely* early WIP library for easily creating REST-based webhook bots for discord using the new Slash Commands feature. 

Powered by FastAPI.



## Example

```python


from dispike.models.incoming import IncomingDiscordInteraction # For Type Hinting
from dispike.response import DiscordResponse

from dispike import Dispike

bot = Dispike(client_public_key="< Public Key >")



# Now build your bot.

# Arguments that you pass to your function are 
# the same arugments you defined/registered with discord..
# Don't forget to have an argument for a ctx (context). 

@bot.interaction.on("sendmessage")	
async def testing(message: str, ctx: IncomingDiscordInteraction):	
    logger.info("Emitted.")	

    logger.debug(ctx.member.user.id)	
    logger.debug(ctx.member.roles)	

    _response = DiscordResponse()	
    _response.content = f"Hello, {ctx.member.user.username}! Your message was {message}"	


    embed = Embed()
    embed.title = "Test"
    embed.add_field(name="Message", value="Value")

    _response.add_new_embed(
        embed
    )

    return _response.response


# Run your bot.
# Powered by uvicorn.

bot.run(port=5000)
    
```
## Result

<p >
    <img
      alt="Website"
      src="./docs/images/demo.png"
    />
</p>


When configuring your endpoint on discord settings, be sure to append ``/interactions`` to your domain.

<p >
    <img
      alt="Website"
      src="./docs/images/domain.png"
    />
</p>

## Caveats

- Does not handle registring new commands.
- Does not handle anything other then string responses. (However you are free to return any valid dict in your handler.)
- Not on PyPi
- Does not speak over the discord gateway. You'll need a server to handle requests and responses.
- Python 3.6+