from pydantic import BaseModel
import typing


class RoleTags(BaseModel):
    bot_id: typing.Optional[typing.Any]
    intergration_id: typing.Optional[typing.Any]
    permium_subscriber = typing.Optional[typing.Any]


class Role(BaseModel):
    id: int
    name: str
    color: str
    hoist: bool
    position: int
    permissions: str
    managed: str
    mentionable: bool
    tags: typing.Optional[RoleTags]