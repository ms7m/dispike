# Subcommands

Subcommands are more advanced form of creating bots, and it's recommended that you read the discord documentation before coming here.
Subcommands follow a similar structure as standard commands.

```python


later_response_command = DiscordCommand(
    name="news",
    description="Get news!",
    options=[

        CommandOption(
            name="top",
            description="Get the top news.",
            type=1,
            options=[

                CommandOption(
                    name="Country",
                    description="Get news for a country!",
                    type=CommandTypes.STRING,
                    required=False,
                    choices=[
                        CommandChoice(name="United States", value="us"),
                        CommandChoice(name="Canada", value="ca"),
                        CommandChoice(name="Australia", value="au"),
                        CommandChoice(name="United Kingdom", value="gb"),
                        CommandChoice(name="France", value="fr"),
                        CommandChoice(name="South Korea", value="kr"),
                        CommandChoice(name="Germany", value="de"),
                    ],
                ),
            ],
        )
    ],
)

```
???+ info
	Notice the structure, it's more "nested". The discord documentation has a diagram explaining the correct structure. 



Above example will create

```
/news top <country>

```

<p align="center">
  <img src="../images/exampleChoicesSubcommand.png" alt="commandchoicesselection"></a>
</p>

???+ warning
	Remember to properly write your handler to account for optional arguments.
