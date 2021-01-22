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

    """Easy access to command types.

    Attributes:
        BOOLEAN (int): Represents Type 5
        CHANNEL (int): Represents Type 7
        INTEGER (int): Represents Type 4
        ROLE (int): Represents Type 8
        STRING (int): Represents Type 3
        SUB_COMMAND (int): Represents Type 1
        SUB_COMMAND_GROUP (int): Represents Type 2
        USER (int): Represents Type 6
    """

    SUB_COMMAND = 1
    SUB_COMMAND_GROUP = 2
    STRING = 3
    INTEGER = 4
    BOOLEAN = 5
    USER = 6
    CHANNEL = 7
    ROLE = 8


class CommandChoice(BaseModel):

    """Represents a key-value command choice."""

    name: str
    value: str


class CommandOption(BaseModel):

    """Represents a standard command option (not a subcommand)."""

    class Config:
        arbitrary_types_allowed = True

    name: str
    description: str
    type: int
    required: bool = False
    choices: typing.Optional[
        typing.Union[typing.List[dict], typing.List[CommandChoice]]
    ] = None

    options: typing.Optional[
        typing.Union[typing.List[CommandChoice], typing.List]
    ] = None

    # @validator("options")
    # def options_allow_only_if_subcommand(cls, v):
    #   if cls.type != 1:
    #       raise ValidationError("Type must be 1 in order to have options.")
    #   return v


class SubcommandOption(BaseModel):

    """Represents a subcommand, usually you would put this as an option in a DiscordCommand"""

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
                raise ValueError(
                    f"CommandOptions <{item.name}> located <{item_location}> must be have type of 1 due to parent being a subcommand."
                )
        return v


class DiscordCommand(BaseModel):

    """Represents a discord command."""

    id: typing.Optional[int]
    name: str
    description: str
    options: typing.List[typing.Union[SubcommandOption, CommandOption]]
