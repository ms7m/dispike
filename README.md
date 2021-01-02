# dispike

***
[![codecov](https://codecov.io/gh/ms7m/dispike/branch/master/graph/badge.svg?token=E5AXLZDP9O)](https://codecov.io/gh/ms7m/dispike) ![Test Dispike](https://github.com/ms7m/dispike/workflows/Test%20Dispike/badge.svg?branch=master) ![PyPi Link](https://img.shields.io/badge/Available%20on%20PyPi-Dispike-blue?logo=pypi&link=%22https://pypi.org/project/dispike%22) ![PyPiVersion](https://img.shields.io/badge/dynamic/json?color=blue&label=PyPi%20Version&query=%24.info.version&url=https%3A%2F%2Fpypi.org%2Fpypi%2Fdispike%2Fjson) ![Docs](https://img.shields.io/badge/Docs-Available-lightgrey?link=https://dispike.ms7m.me/) 

***



an *extremely-extremely* early WIP library for easily creating REST-based webhook bots for discord using the new Slash Commands feature. 

Powered by FastAPI.


***

## Learn more
- Read documentation [here](https://dispike.ms7m.me)
- See example bot [here](https://github.com/ms7m/dispike-example-bot)




## Caveats

- ~~Does not handle registring new commands.~~
- ~~Does not handle anything other then string responses. (However you are free to return any valid dict in your handler.)~~
- ~~Not on PyPi~~
- Does not speak over the discord gateway. You'll need a server to handle requests and responses.
- Python 3.6+
- Does not support the following endpoints
  - [Create Followup Message](https://discord.com/developers/docs/interactions/slash-commands#create-followup-message)
  - [Edit Followup Message](https://discord.com/developers/docs/interactions/slash-commands#edit-followup-message)
  - [Delete Followup Message](https://discord.com/developers/docs/interactions/slash-commands#delete-followup-message)
- Handling followup messages.



# Development

Help is wanted in mantaining this library. Please try to direct PRs to the ``dev`` branch, and use black formatting (if possible).

![Test Dispike](https://github.com/ms7m/dispike/workflows/Test%20Dispike/badge.svg?branch=dev)
