# dispike

***
[![codecov](https://codecov.io/gh/ms7m/dispike/branch/master/graph/badge.svg?token=E5AXLZDP9O)](https://codecov.io/gh/ms7m/dispike) ![Test Dispike](https://github.com/ms7m/dispike/workflows/Test%20Dispike/badge.svg?branch=master) [![PyPi Link](https://img.shields.io/badge/Available%20on%20PyPi-Dispike-blue?logo=pypi&link=%22https://pypi.org/project/dispike%22)](http://pypi.org/project/dispike) ![PyPiVersion](https://img.shields.io/badge/dynamic/json?color=blue&label=PyPi%20Version&query=%24.info.version&url=https%3A%2F%2Fpypi.org%2Fpypi%2Fdispike%2Fjson) [![Docs](https://img.shields.io/badge/Docs-Available-lightgrey?link=https://dispike.ms7m.me/)
](http://dispike.ms7m.me)

***



an *extremely* early WIP library for easily creating REST-based webhook bots for discord using the new Slash Commands feature.

Powered by [FastAPI](https://github.com/tiangolo/fastapi).


***


## Install

```
pip install dispike
```

## Learn more
- Read documentation [here](https://dispike.ms7m.me)
- See an example bot [here](https://github.com/ms7m/dispike-example)

## Example Code

```python

from dispike import Dispike
bot = Dispike(..)

@bot.interaction.on("stock"):
async def handle_stock_request(stockticker: str, ctx: IncomingDiscordInteraction) -> DiscordResponse:
  get_price = function(stockticker...)
  
  embed=discord.Embed()
  embed.add_field(name="Stock Price for {stockticker}.", value="Current price is {get_price}", inline=True)
  embed.set_footer(text="Request received by {ctx.member.user.username}")
  return DiscordResponse(embed=embed)



if __name__ == "__main__":
    bot.run()
```



## Caveats

- Python 3.6+
- Does not speak over the discord gateway. [discord-py-slash-command is what you are looking for.](https://github.com/eunwoo1104/discord-py-slash-command)

<details><summary>Resolved Caveats</summary>
<p>

- ~~Does not handle registring new commands.~~
- ~~Does not handle anything other then string responses. (However you are free to return any valid dict in your handler.)~~
- ~~Not on PyPi~~
- ~~Handling followup messages.~~

</p>
</details>




# Development

Help is wanted in mantaining this library. Please try to direct PRs to the ``dev`` branch, and use black formatting (if possible).

![Test Dispike](https://github.com/ms7m/dispike/workflows/Test%20Dispike/badge.svg?branch=dev)

# Special Thanks
- [Squidtoon99](https://github.com/Squidtoon99)
