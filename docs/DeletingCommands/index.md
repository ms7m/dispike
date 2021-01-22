# Deleting Commands

Deleting commands is similar to [Editing Commands](../EditingCommands/index.md) except ``new_command`` parameter is not available. 

Simply pass the command id instead. Pair this with getting commands and you should be good to go in finding what specific commands to delete.


```python

from dispike import Dispike

bot = Dispike(...)

bot.delete_command(
    command_id=12345
)
```

****

# API Reference

:::dispike.main.Dispike.delete_command
