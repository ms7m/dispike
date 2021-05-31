# Editing Commands

Editing commands require an already initialized ``Dispike`` instance and are available as a method provided by ``Dispike``.

Bulk editing is available by setting the ``bulk`` parameter to ``True`` and passing a list of ``DiscordCommand`` to the ``new_command`` parameter.  

Editing a single command can be done by passing a ``DiscordCommand`` to ``new_command`` and specifying the target command ID.


Guild-level editing command is available by configuring parameters

- ``guild_only`` -> ``True``
- ``guild_id_passed`` -> GUILD ID

??? info
    Follow [this Discord guide to find your server/guild ID](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-)
***



```python

from dispike import Dispike
from dispike.register.models import (
    DiscordCommand
)


bot = Dispike(...)

bot.edit_command(
    new_command=DiscordCommand(...),
    command_id=12345
)

```


```python
from dispike import Dispike
from dispike.register.models import DiscordCommand


bot = Dispike(...)

edit_bulk_commands = [DiscordCommand(...), DiscordCommand(...)]

bot.edit_command(
    new_command=edit_bulk_commands,
    bulk=True
)
```



# API Reference

***

:::dispike.main.Dispike.edit_command



# Handling Permissions

Permissions are a new feature in Discord that allow bot developers to add permissions for a command. 

Dispike can help you 
- View permissions for a command in a guild.
- Craft the correct syntax for setting a permission (or multiple) for a command.

## Preface
[It's helpful that you read the documentation for Discord to understand how to craft permissions.](https://discord.com/developers/docs/interactions/slash-commands#permissions). 
Not reading the documentation may result in you creating dangerous commands for a server!

## Getting Started
Import the following:
```python
from dispike.register.models.permissions import (
    ApplicationCommandPermissions,
    NewApplicationPermission,
    ApplicationCommandPermissionType,
)
```



### Sample Code

```python
new_permission = NewApplicationPermission(
    permissions=[
        ApplicationCommandPermissions(
            id="<Discord User Id>",
            type=ApplicationCommandPermissionType.USER,
            permission=True, # Whether to determine if the user has permission.
        )
    ]
)

get_commands = bot.get_commands(guild_only=True, guild_id_passed="<Guild ID>")
selected_command = get_commands[0]


update_permission_for_command = bot.set_command_permission(
		command_id=selected_command.id # also can be passed manually
  	guild_id="<Guild ID>",
    new_permission
)

print(update_permission_for_command)
>> True

```



The example above starts out with creating a new command using ``NewApplicationPermission``.  If you read the documentation, it should look familiar to the example provided by Discord -- except for the type that is passed. 

You can manually use a normal ``int`` value for ``type`` parameter, otherwise you can use a helper class called ``ApplicationCommandPermissionType``. 

:::dispike.register.models.permissions.ApplicationCommandPermissionType



???+ info

​	Remember -- You are able to have multiple permissions as the ``permissions`` parameter is a ``List``. However you should note Discord's docs about how certain permissions may conflict and throw an error. In a future version dispike may alert you of offending permissions, but for now keep in mind.



Afterwards, we need a command to edit, we check this by gathering every command in a guild. If you are not familiar with this, you can read more [here](/GettingCommands). 



There is a function available in the bot instance that will allow you to update a commands permission. This function is also available in sync & async.

:::dispike.main.Dispike.set_command_permission

