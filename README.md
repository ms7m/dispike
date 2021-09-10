<div align="center">
<br>
  <h1> dispike </h1>
  <i> ⚙️  A simple to use, powerful framework for creating stateless, independent bots using <a href="https://discord.com/developers/docs/interactions/slash-commands"> Discord Slash Commands.</a> </i>
  <br>
  <br>
    <a > ⚡ Powered by <a href="https://github.com/tiangolo/fastapi"> FastAPI.</a> </a>
  <br>
  <br>
  <p align="center">
    <img src="https://codecov.io/gh/ms7m/dispike/branch/master/graph/badge.svg?token=E5AXLZDP9O">
    <img src="https://github.com/ms7m/dispike/workflows/Test%20Dispike/badge.svg?branch=master">
    <img src="https://img.shields.io/badge/Available%20on%20PyPi-Dispike-blue?logo=pypi&link=%22https://pypi.org/project/dispike%22">
    <img src="https://img.shields.io/badge/dynamic/json?color=blue&label=PyPi%20Version&query=%24.info.version&url=https%3A%2F%2Fpypi.org%2Fpypi%2Fdispike%2Fjson">
  </p>
  <br>
</div>


## 📦 Installation


**Latest stable-version**
```
pip install dispike
```

## 📚 Learn more
- Read documentation [here](https://dispike.ms7m.me)
- See an example bot [here](https://github.com/ms7m/dispike-example)
- Join our Discord Server [here](https://discord.gg/yGgRmEYjju)

***
<div align="center">
<h2> 🧑‍💻 Quick Start Examples </h2>
</div>


### Basic

```python

from dispike import Dispike, DiscordCommand, DiscordResponse
from dispike import IncomingDiscordSlashInteraction
from dispike.helper import Embed

bot = Dispike(...)


command = DiscordCommand(
  name="stock", description="Get the latest active stocks in the market!"
)


@bot.on("stock")
async def handle_stock_request(stockticker: str, ctx: IncomingDiscordSlashInteraction) -> DiscordResponse:
  get_price = function(stockticker...)
  
  embed=Embed()
  embed.add_field(name="Stock Price for {stockticker}.", value="Current price is {get_price}", inline=True)
  embed.set_footer(text="Request received by {ctx.member.user.username}")
  return DiscordResponse(embed=embed)



if __name__ == "__main__":
    bot.register(command)
    bot.run()
```


### Advanced

```python
import dispike
from dispike import interactions, DiscordCommand, DiscordResponse
from dispike import IncomingDiscordSlashInteraction
from dispike.helper import Embed


class SampleGroupCollection(interactions.EventCollection):

    def __init__(self):
        self._api_key = "..."

    def command_schemas(self):
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
    async def latest_stocks(self, ctx: IncomingDiscordSlashInteraction) -> DiscordResponse:
        embed = Embed()

        # check user's porfolio by looking in the database by their discord ID
        portfolio_stats = self.get_portfolio_stats(
            ctx.member.user.id
        )

        embed.add_field(name="Stocks are doing good!", value=f"Current portfolio is {portfolio_stats}", inline=True)
        embed.set_footer(text="Request received by {ctx.member.user.username}")
        return DiscordResponse(embeds=[embed])

    @interactions.on("price")
    async def get_stock_price(self, ctx: IncomingDiscordSlashInteraction, ticker: str) -> DiscordResponse:
        embed = Embed()
        embed.add_field(name=f"Stock Price for 1.",
                        value=f"Current price is {self.get_stock_information(ticker)}", inline=True)
        embed.set_footer(text="Request received by {ctx.member.user.username}")
        return DiscordResponse(embeds=[embed])

## Inside seperate file

from dispike import Dispike, DiscordCommand

bot = Dispike(...)

bot.register_collection(SampleGroupCollection(), register_command_with_discord=True)

if __name__ == "__main__":
    bot.run(port=5000)
```

## Discord API Coverage
<details><summary>View Coverage</summary>
<p>

| API Endpoint   |      Implementation   |
|----------|:-------------:|
| Get Global Application Commands |  **✅ Implemented** |
| Create Global Application Command |    **✅ Implemented**   |
| Edit Global Application Command |  **✅ Implemented** |
| Delete Global Application Command | **✅ Implemented** |
| Create Guild Application Command | **✅ Implemented** |
| Edit Guild Application Command | **✅ Implemented** |
| Delete Guild Application Command | **✅ Implemented** |
| Create Interaction Response | **✅ Implemented** |
| Edit Original Interaction Response | **✅ Implemented**|
| Delete Original Interaction Response | **✅ Implemented** |
| Create Followup Message |**✅ Implemented** |
| Edit Followup Message | **✅ Implemented** |
| Delete Followup Message | **✅ Implemented** |
| Data Models and Types | **✅ Implemented** |
| ApplicationCommand | **✅ Implemented** |
| ApplicationCommandOption | **✅ Implemented** |
| ApplicationCommandOptionType | **✅ Implemented** |
| ApplicationCommandOptionChoice | **✅ Implemented** |
| Interaction | **✅ Implemented** |
| Interaction Response | **✅ Implemented** |
| Message Components | **✅ Implemented** |
| Buttons (Message Components) | **✅ Implemented** |
| Action Rows (Message Components) | **✅ Implemented** |
| Message Select (Message Components) | **✅ Implemented** |

</p>
</details>

## ℹ️ Notice

- Python 3.6+
- Does not speak over the discord gateway. [discord-py-slash-command is what you are looking for.](https://github.com/eunwoo1104/discord-py-slash-command). 
- You will need a server to accept connections directly from discord!


## 🧑‍💻 Development

Help is wanted in mantaining this library. Please try to direct PRs to the ``dev`` branch, and use black formatting (if possible).

# 🎉 Special Thanks
- [Squidtoon99](https://github.com/Squidtoon99)
- [marshmallow](https://github.com/mrshmllow)
