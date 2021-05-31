from enum import Enum
from pydantic import BaseModel, conlist
import typing
import dataclasses


if typing.TYPE_CHECKING:  # pragma: no cover
    static_check_init_args = dataclasses.dataclass
else:

    def static_check_init_args(cls):
        return cls


class AllowedMentionTypes(str, Enum):
    ROLE_MENTIONS = "roles"
    USER_MENTIONS = "users"
    EVERYONE_MENTIONS = "everyone"


@static_check_init_args
class AllowedMentions(BaseModel):
    parse: typing.List[AllowedMentionTypes]
    roles: conlist(str, max_items=100) = []
    users: conlist(str, max_items=100) = []
    replied_user: bool = False
