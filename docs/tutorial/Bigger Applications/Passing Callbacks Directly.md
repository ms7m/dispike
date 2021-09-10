# Passing Callbacks Directly

If you choose not to use ``EventCollections`` directly, you can pass any async function.

```python
from dispike import interactions

async def sample(...):
  return ...
  

  
from dispike import Dispike

bot = Dispike(...)
bot.register_event_command(
	function_event_name="sample",
  function=sample,
  function_type=EventTypes.COMMAND
)

```

:::dispike.main.Dispike.register_event_command

