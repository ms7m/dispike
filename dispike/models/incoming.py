from pydantic import BaseModel, ValidationError, validator
import typing
from .discord_types.member import Member

from ..register.models import CommandOption, SubcommandOption

try:
    from typing import Literal  # pragma: no cover
except ImportError:  # pragma: no cover
    # backport
    from typing_extensions import Literal  # pragma: no cover


class IncomingDiscordOption(BaseModel):

    """An incoming discord option, this is not intended for you to edit, and will not
    be accepted as an argument in any function nor will be accepted as a value in DiscordCommand

    Attributes:
        name (str): Name of the option
        value (str): Value of the option
    """

    name: str
    value: str


class SubcommandIncomingDiscordOptionListChild(BaseModel):

    """
    Attributes:
        name (str): Name of the subcommand
        options (List[IncomingDiscordOption]], optional): Options selected by the user
    """

    class Config:
        arbitary_types_allowed = True

    name: str
    options: typing.List[IncomingDiscordOption]


class SubcommandIncomingDiscordOptionList(BaseModel):

    """An incoming discord option list, this is not intended for you to edit, and will not
    be accepted as an argument in any function nor accepted in DiscordCommand

    Attributes:
        name (str): Name of the subcommand
        options (Union[List[IncomingDiscordOption], List[SubcommandIncomingDiscordOptionListChild]], optional): Options selected by the user
    """

    class Config:
        arbitary_types_allowed = True

    name: str
    options: typing.Union[
        typing.List[IncomingDiscordOption],
        typing.List[SubcommandIncomingDiscordOptionListChild],
    ]


class IncomingDiscordOptionList(BaseModel):

    """An incoming discord option list, this is not intended for you to edit, and will not
    be accepted as an argument in any function nor accepted in DiscordCommand

    Attributes:
        id (str): Id of the command
        name (str): Name of the command
        options (Union[List[IncomingDiscordOption], List[SubcommandIncomingDiscordOptionList]], optional): Options selected by the user
    """

    class Config:
        arbitary_types_allowed = True

    id: str
    name: str
    options: typing.Optional[
        typing.Union[
            typing.List[IncomingDiscordOption],
            typing.List[SubcommandIncomingDiscordOptionList],
        ]
    ] = None


class IncomingDiscordButtonData(BaseModel):

    """
    Incoming button data.

    Attributes:
        custom_id (str): The custom id of this button.
    """

    custom_id: str


class IncomingDiscordSelectMenuData(BaseModel):

    """
    Incoming select menu data.

    Attributes:
        custom_id (str): The custom id of this button.
        values (List[str]): A list of string values that the user selected.
    """

    custom_id: str
    values: typing.List[str]


class IncomingDiscordInteraction(BaseModel):

    """An incoming discord interaction that was triggered by a command, this is not intended for you to edit, and will not
    be accepted as an argument in any function.

    Attributes:
        id (int): Id of the interaction.
        data (IncomingDiscordOptionList): Options from the command.
        guild_id (int): Guild ID where this happened.
        channel_id (int): Channel ID where this happened.
        member (Member): Member that used this interaction.
        token (str): Token of this interaction.
    """

    class Config:
        arbitary_types_allowed = True

    type: Literal[2, 3, 4, 5, 6, 7, 8]  # 1 is removed, this lib will handle PING
    id: int
    data: IncomingDiscordOptionList
    guild_id: int
    channel_id: int
    member: Member
    token: str
    version: typing.Optional[Literal[1]] = None


class IncomingDiscordButtonInteraction(BaseModel):

    """An incoming discord interaction that was triggered by a button press, this is not intended for you to edit, and will not
    be accepted as an argument in any function.

    Attributes:
        id (int): Id of the interaction.
        data (IncomingDiscordButtonData): Data from the interaction.
        guild_id (int): Guild ID where this happened.
        channel_id (int): Channel ID where this happened.
        member (Member): TODO: IDK if this is the member that called the command originally or the one that used the button.
        token (str): Token of this interaction.
    """

    type: Literal[2, 3, 4, 5, 6, 7, 8]  # 1 is removed, this lib will handle PING
    id: int
    data: IncomingDiscordButtonData
    guild_id: int
    channel_id: int
    member: Member
    token: str
    version: typing.Optional[Literal[1]] = None


class IncomingDiscordSelectMenuInteraction(BaseModel):

    """An incoming discord interaction that was triggered by a select menu interaction, this is not intended for you to edit, and will not
    be accepted as an argument in any function.

    Attributes:
        id (int): Id of the interaction.
        data (IncomingDiscordSelectMenuData): Data from the interaction.
        guild_id (int): Guild ID where this happened.
        channel_id (int): Channel ID where this happened.
        member (Member): TODO: IDK if this is the member that called the command originally or the one that used the select menu.
        token (str): Token of this interaction.
    """

    type: Literal[2, 3, 4, 5, 6, 7, 8]  # 1 is removed, this lib will handle PING
    id: int
    data: IncomingDiscordSelectMenuData
    guild_id: int
    channel_id: int
    member: Member
    token: str
    version: typing.Optional[Literal[1]] = None


class IncomingApplicationCommand(BaseModel):

    """An Incoming Application command, this is not intended for you to edit, and will not be accepted
    in any function

    Attributes:
        id (int): Id of the interaction.
        application_id (int): The id of your bot.
        name (int): Name of the command.
        description (int): Description of the command.
        options (Union[List[CommandOption], List[SubcommandOption]], optional): Selected options from the command.
        default_permission (bool, optional): Bool whether if uses default permissions.
    """

    class Config:
        arbitary_types_allowed = True

    id: int
    application_id: int
    name: str
    description: str
    options: typing.Optional[
        typing.Union[typing.List[CommandOption], typing.List[SubcommandOption]]
    ]
    default_permission: typing.Optional[bool]

    # ? not listed in docs but appears in request
    version: typing.Optional[str]
