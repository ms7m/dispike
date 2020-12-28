from pydantic import BaseModel, validator, Extra
import typing
from pydantic.error_wrappers import ValidationError

from pydantic.errors import ArbitraryTypeError


try:
    from typing import Literal
except ImportError:
    # backport
    from typing_extensions import Literal


class CommandTypes:
    SUB_COMMAND = 1
    SUB_COMMAND_GROUP = 2
    STRING = 3
    INTEGER = 4
    BOOLEAN = 5
    USER = 6
    CHANNEL = 7
    ROLE = 8


class CommandChoice(BaseModel):
    name: str
    value: str


class CommandOption(BaseModel):
    class Config:
        arbitrary_types_allowed = True
        extra = Extra.allow

    name: str
    description: str
    type: int
    required: bool = False
    choices: typing.Optional[
        typing.Union[typing.List[dict], typing.List[CommandChoice]]
    ] = []

    # options: typing.Optional[typing.Union[typing.List[CommandChoice]]]

    # @validator("options")
    # def options_allow_only_if_subcommand(cls, v):
    #    if cls.type != 1:
    #        raise ValidationError("Type must be 1 in order to have options.")
    #    return v


class SubcommandOption(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    name: str
    description: str
    type: Literal[2] = 2
    options: typing.List[CommandOption]

    @validator("options")
    def options_must_contain_type_1(cls, v):  # pylint: disable=no-self-argument
        item: CommandOption
        for item_location, item in enumerate(v):
            if item.type != 1:
                raise ValidationError(
                    f"CommandOptions located in <{item_location}> must be have type of 1 due to parent being a subcommand."
                )
        return v


class DiscordCommand(BaseModel):
    name: str
    description: str
    options: typing.List[typing.Union[SubcommandOption, CommandOption]]
