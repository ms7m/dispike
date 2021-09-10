import dataclasses
import typing

from pydantic import BaseModel, Extra, validator, root_validator
from pydantic.error_wrappers import ValidationError
from pydantic.errors import ArbitraryTypeError
from enum import Enum

try:
    from typing import Literal  # pragma: no cover
except ImportError:  # pragma: no cover
    # backport
    from typing_extensions import Literal  # pragma: no cover

if typing.TYPE_CHECKING:  # pragma: no cover
    static_check_init_args = dataclasses.dataclass
else:

    def static_check_init_args(cls):
        return cls


class OptionTypes(int, Enum):
    """Easy access to option types.

    Attributes:
        BOOLEAN (int): Represents Type 5
        CHANNEL (int): Represents Type 7
        INTEGER (int): Represents Type 4
        ROLE (int): Represents Type 8
        STRING (int): Represents Type 3
        SUB_COMMAND (int): Represents Type 1
        SUB_COMMAND_GROUP (int): Represents Type 2
        USER (int): Represents Type 6
        MENTIONABLE (int): Represents Type 9
        NUMBER (int): Represents Type 10
    """

    SUB_COMMAND = 1
    SUB_COMMAND_GROUP = 2
    STRING = 3
    INTEGER = 4
    BOOLEAN = 5
    USER = 6
    CHANNEL = 7
    ROLE = 8
    MENTIONABLE = 9
    NUMBER = 10


class CommandTypes(int, Enum):
    """Easy access to command types.

    Attributes:
        SLASH (int): Represents Type 1
        USER (int): Represents Type 2
        MESSAGE (int): Represents Type 3
    """

    SLASH = 1
    USER = 2
    MESSAGE = 3


@static_check_init_args
class CommandChoice(BaseModel):

    """Represents a key-value command choice.

    Attributes:
        name (str): Name of the choice.
        value (str): Value of the choice.
    """

    name: str
    value: typing.Union[str, int, float]


@static_check_init_args
class CommandOption(BaseModel):

    """Represents a standard command option (not a subcommand).

    Attributes:
        name (str): Name of the option.
        description (str): Description of the option.
        type (OptionTypes): The option type.
        required (bool): Whether or not this option is required.
        choices (typing.Union[typing.List[dict], typing.List[CommandChoice]], optional): Possible choices for this option for the user to pick from.
        options (typing.Union[typing.List[CommandChoice], typing.List], optional): If the option is a subcommand or subcommand group type, this nested options will be the parameters.
    """

    class Config:
        arbitrary_types_allowed = True

    name: str
    description: str
    type: OptionTypes
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


@static_check_init_args
class SubcommandOption(BaseModel):

    """Represents a subcommand group usually you would put this as an option in a DiscordCommand

    Attributes:
        name (str): Name of this group.
        description (str): Description of this group.
        options (typing.List[CommandOption]): Options for this group.
    """

    class Config:
        arbitrary_types_allowed = True

    name: str
    description: str
    options: typing.List[CommandOption]
    type: Literal[2] = 2

    # @validator("options", pre=True, always=True)
    # def options_must_contain_type_1(cls, v):  # pylint: disable=no-self-argument
    #    item: CommandOption
    #    for item_location, item in enumerate(v):
    #        if isinstance(item, CommandOption):
    #            _type = item.type
    #            _error_name = item.name
    #        elif isinstance(item, dict):
    #            _type = item["type"]
    #            _error_name = item["name"]
    #
    #        if _type != 1:
    #            raise ValueError(
    #                f"CommandOptions <{_error_name}> located <{item_location}> must be have type of 1 due to parent being a subcommand."
    #            )
    #    return v


@static_check_init_args
class DiscordCommand(BaseModel):

    """Represents a discord command.

    Attributes:
        id (int, optional): Id of this command.
        name (str): Name of this command.
        description (str): Description of this command.
        options (typing.List[typing.Union[SubcommandOption, CommandOption]]): Options for this command.
        default_permission (boolean): whether the command is enabled by default when the app is added to a guild. Defaults to True.
        type (Union[CommandTypes, int]): The type of command. This defaults to SLASH
    """

    id: typing.Optional[int]
    name: str
    description: str = ""
    options: typing.List[typing.Union[SubcommandOption, CommandOption]] = []
    default_permission: bool = True
    type: typing.Union[CommandTypes, int] = CommandTypes.SLASH

    @root_validator
    def validate_correct_type_requirements(cls, values):
        _cls_type, _cls_description, _cls_options = (
            values.get("type"),
            values.get("description"),
            values.get("options"),
        )
        if _cls_type == CommandTypes.SLASH:
            if _cls_description == "":
                raise ValueError("Slash commands require a description")
        if _cls_type == CommandTypes.MESSAGE or _cls_type == CommandTypes.USER:
            if _cls_description != "":
                raise ValueError("Context commands cannot have a description")
            if _cls_options:
                raise ValueError("Context commands cannot have options")

        return values

    @validator("type", pre=True, always=True)
    def set_value_type(cls, v):
        if isinstance(v, CommandTypes):
            return v.value
        return v
