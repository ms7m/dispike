# Preface



Writing a handler function is required to properly route interactions from the user to your bot. After request verification, the request (interaction) is passed to an ``IncomingDiscordInteraction`` object. You will write your handler as a function to directly accept an additional argument called ``ctx`` containing this interaction.

It's normal not to use this interaction, it only exists to give you context about the interaction.



### Writing the handler.

Your handler must be 

- Async (``async def``)

- Accept the same number of arguments (if any) as the command with an additional argument for the context. 

  - ```python
    async def ...(argument_one, argument_two, ctx) -> ...
    ```

- Contain a ``bot.on(<command-identifier>, <event type>)`` decorator.

  OR

- Contain ``dispike.interactions.on(<command-identifier>, <event type>)`` decorator



### Finding the command identifier.



#### Normal commands

Finding the command identifier is simple. If you are writing a normal (non-subcommand) command, it's often just the command name.

```json
command_to_be_registered = DiscordCommand(
    name="wave", # this is the main command name.,
    description="Send a wave to a nice person! 👋 ",
    options=[
        CommandOption(
            name="person", # this is the attribute assigned to the value passed.,
            description="person to target", # this describes the value to pass,
          	required=True,
            type=CommandTypes.USER
        )
    ]
)
```

The command identifier in this case will be ``wave``. 

```python
@bot.interaction.on("wave", EventTypes.COMMAND)
async def handle_wave(person, ctx) -> DiscordResponse:
    ...
```



#### Subcommands

Subcommands are similar but are more "nested". Each layer will be represented and separated by a ``.``

Take a look at this command that was registered

```python
command_configuration = DiscordCommand(
    name="forex",
    description="Get Forex rates",
    options=[
        SubcommandOption(
            name="latest",
            description="Get latest forex rates.",
            type=2,
            options=[
                CommandOption(
                    name="convert",
                    description="View rates between two symbols.",
                    type=1,
                    required=False,
                    options=[
                        {
                            "name": "symbol_1",
                            "description": "Symbol 1",
                            "type": CommandTypes.STRING,
                            "required": True,
                        },
                        {
                            "name": "symbol_2",
                            "description": "Symbol 2",
                            "type": CommandTypes.STRING,
                            "required": False,
                        },
                    ],
                )
            ],
        )
    ],
)
```

When a user uses this command in discord. They'd use it as

```
/forex latest convert <SYMBOL 1> <SYMBOL 2>
```

The command identifier would be represented as

``forex.latest.convert``



## Buttons and Select Menus

Finding the command identifier for buttons or select menus can be found by finding the ``custom_id`` attribute in either ``Buttons`` or ``SelectMenu``.



***



# Defining the arguments



**You must define the same number of arguments in your python function as the discord command**. 

???+ warning
	If you have an optional argument, you can pass the ``**kwargs`` argument to your function. Learn more about the ``*kwargs`` argument [here](https://book.pythontips.com/en/latest/args_and_kwargs.html). If the user adds an optional argument, this will be passed to the function. Otherwise, it will not be present. Write your code to check if it exists before doing anything!



The command argument names must match to the one set as the ``value`` when registering your command.



```python
@bot.interaction.on("forex.latest.convert", EventTypes.COMMAND)
async def handle_forex_convert(symbol_1: str, symbol_2: str, ctx: IncomingDiscordInteraction) -> DiscordResponse:
    ...
```

