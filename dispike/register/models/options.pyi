import typing

# TODO: Automate stub generation until upstream issue fix.

class CommandChoice:
    def __init__(self, name: str, value: str) -> None: ...

class CommandOption:
    def __init__(
        self,
        name: str,
        description: str,
        type: int,
        choices: typing.Union[
            typing.Union[typing.List[dict], typing.List[CommandChoice]]
        ],
        required: bool = False,
    ) -> None: ...

class SubcommandOption:
    def __init__(
        self,
        name: str,
        description: str,
        options: typing.List[CommandOption],
        type: typing.Literal[2] = 2,
    ) -> None: ...

class DiscordCommand:
    def __init__(
        self,
        name: str,
        description: str,
        options: typing.List[typing.Union[SubcommandOption, CommandOption]],
    ) -> None: ...
