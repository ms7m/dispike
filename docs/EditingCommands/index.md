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
