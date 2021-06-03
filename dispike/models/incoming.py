from enum import Enum
from pydantic import BaseModel, Json, ValidationError, validator
import typing
from .discord_types.member import Member
from .discord_types.component import ComponentType

from ..register.models import CommandOption, SubcommandOption

try:
    from typing import Literal  # pragma: no cover
except ImportError:  # pragma: no cover
    # backport
    from typing_extensions import Literal  # pragma: no cover


class InteractionType(int, Enum):
    APPLICATION_COMMAND = 2
    MESSAGE_COMPONENT = 3


class IncomingDiscordOption(BaseModel):

    """An incoming discord option, this is not intended for you to edit, and will not
    be accepted as an argument in any function nor will be accepted as a value in DiscordCommand
    """

    name: str
    value: str


class SubcommandIncomingDiscordOptionListChild(BaseModel):
    class Config:
        arbitary_types_allowed = True

    name: str
    options: typing.List[IncomingDiscordOption]


class SubcommandIncomingDiscordOptionList(BaseModel):
    """An incoming discord option list, this is not intended for you to edit, and will not
    be accepted as an argument in any function nor accepted in DiscordCommand
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


class IncomingDiscordInteraction(BaseModel):

    """An incoming discord interaction, this is not intended for you to edit, and will not
    be accepted as an argument in any function.
    """

    class Config:
        arbitary_types_allowed = True

    type: InteractionType  # 1 is removed, this lib will handle PING
    id: int
    data: IncomingDiscordOptionList
    guild_id: int
    channel_id: int
    member: Member
    token: str
    version: typing.Optional[Literal[1]] = None
    channel_id: int


class IncomingApplicationCommand(BaseModel):

    """an Incoming Application command, this is not intended for you to edit, and will not be accepted
    in any function
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


class SelectedButtonInteractionData(BaseModel):
    custom_id: typing.Union[int, str]
    component_type: Literal[ComponentType.BUTTON]


class IncomingButtonInteraction(BaseModel):
    class Config:
        arbitary_types_allowed = True

    type: Literal[
        InteractionType.MESSAGE_COMPONENT
    ]  # 1 is removed, this lib will handle PING
    id: int
    guild_id: int
    channel_id: int
    member: Member
    token: str
    version: typing.Optional[Literal[1]] = None
    channel_id: int

    message: typing.Union[dict, Json]  # TODO: Create BaseModel for Discord Messages
    data: SelectedButtonInteractionData
