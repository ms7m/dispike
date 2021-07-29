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
  - You can also view the status of how much this library covers the API!
- See an example bot [here](https://github.com/ms7m/dispike-example)

## Example Code

### Basic

```python

from dispike import Dispike
bot = Dispike(..)


command = DiscordCommand(
  name="stock", description="Get the latest active stocks in the market!"
)


@bot.on("stock"):
async def handle_stock_request(stockticker: str, ctx: IncomingDiscordInteraction) -> DiscordResponse:
  get_price = function(stockticker...)
  
  embed=discord.Embed()
  embed.add_field(name="Stock Price for {stockticker}.", value="Current price is {get_price}", inline=True)
  embed.set_footer(text="Request received by {ctx.member.user.username}")
  return DiscordResponse(embed=embed)



if __name__ == "__main__":
    bot.register(command)
    bot.run()
```


### Advanced
```python
from dispike import Dispike, interactions, DiscordCommand
from dispike import IncomingDiscordInteraction


class SampleGroupCollection(interactions.EventCollection):

  def __init__(self):
    self._api_key = "..."

  def command_schemas():
    return [
      DiscordCommand(
        name="lateststocks", description="Get the highest performing stocks in the market currently!"
      ),
      interactions.PerCommandRegistrationSettings(
                schema=DiscordCommand(
                    name="price",
                    description="return ticker price for server",
                    options=[],
                ),
                guild_id=11111111,
      )
    ]

  def get_stock_information(self, stock_ticker):
    return ...
  def get_portfolio_stats(self, user_id):
    return ...

  @interactions.on("lateststocks")
  async def latest_stocks(self, ctx: IncomingDiscordInteraction) -> DiscordResponse:
    embed=discord.Embed()

    # check user's porfolio by looking in the database by their discord ID
    portfolio_stats = self.get_portfolio_stats(
      ctx.member.user.id
    )

    embed.add_field(name="Stocks are doing good!", value=f"Current portfolio is {portfolio_stats}", inline=True)
    embed.set_footer(text="Request received by {ctx.member.user.username}")
    return DiscordResponse(embed=embed)

  @interactions.on("price")
  async def get_stock_price(self, ctx: IncomingDiscordInteraction, ticker: str) -> DiscordResponse:
  
    embed=discord.Embed()
    embed.add_field(name=f"Stock Price for {stockticker}.", value=f"Current price is {self.get_stock_information(ticker)}", inline=True)
    embed.set_footer(text="Request received by {ctx.member.user.username}")
    return DiscordResponse(embed=embed)    


## Inside seperate file

from dispike import Dispike, DiscordCommad
bot = Dispike(...)

bot.register_collection(SampleGroupCollection(), register_command_with_discord=True)

if __name__ == "__main__":
  bot.run(port=5000)
```
## Attention

- Python 3.6+
- Does not speak over the discord gateway. [discord-py-slash-command is what you are looking for.](https://github.com/eunwoo1104/discord-py-slash-command). 
- You will need a server to accept connections directly from discord!


# Development

Help is wanted in mantaining this library. Please try to direct PRs to the ``dev`` branch, and use black formatting (if possible).

![Test Dispike](https://github.com/ms7m/dispike/workflows/Test%20Dispike/badge.svg?branch=dev)

# Special Thanks
- [Squidtoon99](https://github.com/Squidtoon99)
- [marshmallow](https://github.com/mrshmllow)
