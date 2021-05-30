from pydantic import BaseModel
from enum import Enum
import typing
import dataclasses

if typing.TYPE_CHECKING:  # pragma: no cover
    static_check_init_args = dataclasses.dataclass
else:

    def static_check_init_args(cls):
        return cls


@static_check_init_args
class ApplicationCommandPermissionType(int, Enum):
    ROLE = 1
    USER = 2


@static_check_init_args
class ApplicationCommandPermissions(BaseModel):
    id: int
    type: ApplicationCommandPermissionType
    permission: bool


@static_check_init_args
class GuildApplicationCommandPermissions(BaseModel):
    id: int
    application_id: int
    permissions: typing.List[ApplicationCommandPermissions]


@static_check_init_args
class NewApplicationPermission(BaseModel):
    permissions: typing.List[ApplicationCommandPermissions]