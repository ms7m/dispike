from pydantic import BaseModel, ValidationError, validator
import typing
from .discord_types.member import Member

from ..register.models import CommandOption, SubcommandOption

try:
    from typing import Literal
except ImportError:
    # backport
    from typing_extensions import Literal


class IncomingDiscordOption(BaseModel):
    name: str
    value: str


class IncomingDiscordOptionList(BaseModel):
    class Config:
        arbitary_types_allowed = True

    id: str
    name: str
    options: typing.List[IncomingDiscordOption]


class IncomingDiscordInteraction(BaseModel):
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


class IncomingApplicationCommand(BaseModel):
    class Config:
        arbitary_types_allowed = True

    id: int
    application_id: int
    name: str
    description: str
    options: typing.List[typing.Union[CommandOption, SubcommandOption]]