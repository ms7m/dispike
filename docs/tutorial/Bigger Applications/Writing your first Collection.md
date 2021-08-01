# Writing EventCollections

Import Dispike interactions, this is a module that contains functions, decorators and classes you'll need to create a collection.

```python
from dispike import interactions
```



Create your EventCollection. Create a class and inherit ``interactions.EventCollection``.

```python
class SampleCollection(interactions.EventCollection):
  def __init__(self, ...):
    ...
```

???+ info
	An `__init__` may be used, but you'll need to let Dispike know to initialize it, or initialize it yourself before passing to dispike.

Add your callbacks..

```python

class SampleCollection(interactions.EventCollection):
  def __init__(self, ...):
    ...
    
	@interactions.on("sampleInteractionCommand"):
	async def incoming_interactions_command(ctx: IncomingDiscordInteraction):
		...
	
	@interactions.on("sampleInteractionCommand2"):
	async def incoming_interactions_command_two(ctx: IncomingDiscordInteraction):
	...
	
	@interactions.on("sampleInteractionButton", type=EventTypes.COMPONENT):
	async def inomcing_interaction_button(ctx: IncomingDiscordButtonInteraction):
	...
	
	@interactions.on("sampleInteractionSelectMenu", type=EventType.COMPONENT):
	async def incoming_select_menu_interaction(ctx: IncomingDiscordSelectMenuInteraction):
	...
```

If you followed the tutorial before, this should look extremely familiar. 

## Adding commands.

You can also add commands..  You must expose a function named ``.command_schemas`` and provide a ``List`` containing either ``PerCommandRegistrationSettings`` or ``DiscordCommand`` items.

Dispike offers a helper class called ``PerCommandRegistrationSettings`` located in interactions. This class allows you to select where (guild) command will be registered.

```python

    def command_schemas() -> typing.List[
        typing.Union[PerCommandRegistrationSettings, "DiscordCommand"]
    ]:
        return [
        	DiscordCommand(
    					name="...", description="...", options=[]
					),
					PerCommandRegistrationSettings(schema=DiscordCommand(...), guild_id=1111)
        
        ]
```

You can see in the example above that ``PerCommandRegistrationSettings`` is used to target a specific guild.