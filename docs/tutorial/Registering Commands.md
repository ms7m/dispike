## Registering Commands

We've created the command, we'll need to register the command with Discord.

???+ info
	All methods for editing, deleting, registering, and getting commands share the same method for globally and guild only.

You will need an initialized ``Dispike`` object.

```python

from dispike import Dispike

bot = Dispike(
  client_public_key="..",
  bot_token="..",
  application_id=".."
)

bot.register(command_to_be_created)
```

:::dispike.register.RegisterCommands.register
