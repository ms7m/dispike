
# Getting Commands

Retrieving existing commands require an already initialized Dispike object.

You can specify whether to return commands globally or per guild.

Getting commands is similar to [Editing Commands](../EditingCommands/index.md) except for ``new_command``, ``command_id``, parameters are not available. 

```python
from dispike import Dispike

bot = Dispike(...)

commands = bot.get_commands()

>>> [IncomingApplicationCommand(...), IncomingApplicationCommand(...)]
```

****

# API Reference

:::dispike.main.Dispike.get_commands

