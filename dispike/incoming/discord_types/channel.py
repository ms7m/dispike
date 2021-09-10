from pydantic import BaseModel
from enum import Enum


class ChannelTypes(int, Enum):
    GUILD_TEXT = 0  # a text channel within a server
    DM = 1  # a direct message between users
    GUILD_VOICE = 2  # a voice channel within a server
    GROUP_DM = 3  # a direct message between multiple users
    GUILD_CATEGORY = 4  # an organizational category that contains up to 50 channels
    GUILD_NEWS = (
        5  # a channel that users can follow and crosspost into their own server
    )
    GUILD_STORE = 6  # a channel in which game developers can sell their game on Discord
    GUILD_NEWS_THREAD = 10  # a temporary sub-channel within a GUILD_NEWS channel
    GUILD_PUBLIC_THREAD = 11  # a temporary sub-channel within a GUILD_TEXT channel
    GUILD_PRIVATE_THREAD = 12  # a temporary sub-channel within a GUILD_TEXT channel that is only viewable by those invited and those with the MANAGE_THREADS permission
    GUILD_STAGE_VOICE = 13  # a voice channel for hosting events with an audience


class PartialChannel(BaseModel):
    """A partial representation for a discord channel. This is found in a Application Command Interaction Data Resolved Structure

    Partial Channel objects only have id, name, type and permissions attributes.

    """

    class Config:
        arbitary_types_allowed = True

    id: int
    type: ChannelTypes
    name: str
    permissions: str
