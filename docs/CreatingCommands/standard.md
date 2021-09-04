# Standard Commands

Creating standard commands is easy to create, and follows a similar structure to building it in JSON. 
Dispike assists you in creating a valid JSON, and will provide auto-completion and type hints.

```python

from dispike.creating import (
    DiscordCommand,
    CommandChoice,
    CommandOption,
    CommandTypes,
)

instant_response_command = DiscordCommand(

    name="quote",

    description="Return a quote from a world leader.",

    options=[

        CommandOption(

            name="worldleader",
            description="World leader name",
            required=True,
            type=CommandTypes.STRING,

            choices=[
                CommandChoice(
                    name="President Donald J. Trump", value="donaldtrump"
                ),
                CommandChoice(name="President Xi Jinping", value="xi"),
                CommandChoice(name="Prime Minster Boris Johnson", value="boris"),
                CommandChoice(name="Chancellor Angela Merkel", value="merkel"),
                CommandChoice(name="Prime Minster Yoshihide Suga", value="suga"),
                CommandChoice(name="Prime Minster Jacinda Ardern", value="ardern"),
            ],


        )
    ],
)
```

Above example will create a command 

```
/quote <worldleader>:{list of chocies}
```

A list of choices will presented to the users.

```python
CommandChoice(name="President Donald J. Trump", value="donaldtrump"),
CommandChoice(name="President Xi Jinping", value="xi"),
CommandChoice(name="Prime Minster Boris Johnson", value="boris"),
CommandChoice(name="Chancellor Angela Merkel", value="merkel"),
CommandChoice(name="Prime Minster Yoshihide Suga", value="suga"),
CommandChoice(name="Prime Minster Jacinda Ardern", value="ardern"),
```

<p align="center">
  <img src="../images/exampleChoicesStandard.png" alt="commandchoicesselection"></a>
</p>


Your handler will recieve the ``value`` of the choice. Not the ``name``.
Meaning if I chose ``Chancellor Angela Merkel``, my bot would recieve ``merkel``.





### Creating commands while preventing circular Import loops.

Circular import loops may occur (especially when creating EventCollections, as you attempt to import ``on`` method of your ``Dispike bot, while also attempting to register the event collection). 

Instead of using the ``on`` method on your bot, you can 

```python
from dispike import interactions

@interactions.on(...)
async def handler(...):
  ...
```

Remember to register your event collection with your initialized bot otherwise your events may go unhandled.
