## Configuring commands

Creating a command is very similar to creating it in JSON, however this library will assist you in making sure the outcome is valid schema for Discord. You should still learn how to build commands by reading the documentation on Discord.



Internally this is powered by [pydantic](https://pydantic-docs.helpmanual.io/). There are third-party plugins to intergrate with your favorite IDEs to enable auto-completion when typing. 



???+ caution
	Autocompletion for creating new models under DiscordCommand, CommandChoice, CommandOption, SubcommandOption, CommandTypes **on VSCode is broken.** (follow discussion here [samuelcolvin/pydantic#650](https://github.com/samuelcolvin/pydantic/issues/650), [microsoft/python-language-server#1898](https://github.com/microsoft/python-language-server/issues/1898)). PyCharm appears to work using an external plugin.
	

Let's get started

```python
# Import
from dispike.register.models import DiscordCommand, CommandOption, CommandChoice, CommandTypes

from dispike.register.models import (
  DiscordCommand,
  CommandOption,
  CommandChoice,
  CommandTypes
)

```

These are the *models* that you will need to get started. Think of models as blueprints.

???+ info
	You can go more advanced by also importing [SubcommandOption], but that's more advanced and is not convered in this tutorial.



Let's create a command. The user will interact with this command such as.

```python
/wave <discord user to send wave to>
```

This is simple to create. Let's make it.



```python
command_to_be_created = DiscordCommand(
    name="wave" # this is the main command name.,
    description="Send a wave to a nice person! 👋 ",
    options=[
        CommandOption(
            name="person" # this is the attribute assigned to the value passed.,
            description="person to target" # this describes the value to pass,
          	required=True,
            type=CommandTypes.USER
        )
    ]
)
```



That's it, simple to create. 

Verify that the ``CommandOption.name`` is something you can name in a normal python function. 

Let's move to register this command.



### Source

```python
--8<-- "dispike/register/models/options.py"
```

