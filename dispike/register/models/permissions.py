from pydantic import BaseModel
from enum import Enum
import typing


class ApplicationCommandPermissionType(int, Enum):
    ROLE = 1
    USER = 2


class ApplicationCommandPermissions(BaseModel):
    id: int
    type: ApplicationCommandPermissionType
    permission: bool


class GuildApplicationCommandPermissions(BaseModel):
    id: int
    application_id: int
    permissions: typing.List[ApplicationCommandPermissionType]


class NewApplicationPermission(BaseModel):
    permissions: typing.List[ApplicationCommandPermissions]