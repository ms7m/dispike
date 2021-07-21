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
    """The permission type of the Application Command."""

    ROLE = 1
    USER = 2


@static_check_init_args
class ApplicationCommandPermissions(BaseModel):
    """An individual permission for a command. """

    id: int
    type: ApplicationCommandPermissionType
    permission: bool


@static_check_init_args
class GuildApplicationCommandPermissions(BaseModel):
    """ Returned when fetching the permissions for a command in a guild. """

    id: int
    application_id: int
    permissions: typing.List[ApplicationCommandPermissions]


@static_check_init_args
class NewApplicationPermission(BaseModel):
    permissions: typing.List[ApplicationCommandPermissions]
