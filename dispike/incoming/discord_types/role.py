from pydantic import BaseModel
import typing


"""
class RoleTags(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    bot_id: typing.Optional[typing.Any] = None
    intergration_id: typing.Optional[typing.Any] = None
    permium_subscriber = typing.Optional[typing.Any] = None
"""


class Role(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    id: int
    name: str
    color: str
    hoist: bool
    position: int
    permissions: str
    managed: str
    mentionable: bool
    tags: typing.Optional[typing.Dict] = {}