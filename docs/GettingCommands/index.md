
# Getting Commands

Getting commands is similar to [Editing Commands](../EditingCommands/index.md) except ``new_command``, ``command_id``, parameters is not available. 

```python
from dispike import Dispike

bot = Dispike(...)

commands = bot.get_commands()

>>> [IncomingApplicationCommand(...), IncomingApplicationCommand(...)]
```

****

# API Reference

:::dispike.main.Dispike.get_commands
