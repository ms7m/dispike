import typing
from ..discord_types.member import PartialMember
from ..discord_types.channel import PartialChannel
from ..discord_types.user import User
from ..discord_types.role import Role

from loguru import logger

if typing.TYPE_CHECKING:
    from ..incoming_interactions import IncomingDiscordInteraction


_class_return = {
    "members": PartialMember,
    "channels": PartialChannel,
    "users": User,
    "roles": Role,
}


def resolved_interactions_finder(
    cls: "IncomingDiscordInteraction",
    query: typing.Union[str, int],
    type_to_determine: str,
) -> typing.Union[PartialMember, None]:
    """
    Finds all interactions that are resolved.

    :param query: The query to search for.
    :param type_to_determine: The type of interaction to search for.
    :return: A list of all interactions that are resolved.
    """

    try:
        _grab_member = cls.data.resolved["members"].get(query, None)
        if _grab_member is not None:
            return _class_return[type_to_determine](**_grab_member)
        return _grab_member
    except Exception:
        logger.exception(f"Unable to find query: {query} in resolved interactions..")


def lookup_resolved_member_helper(cls, member_id: str) -> PartialMember:
    return resolved_interactions_finder(cls, member_id, "members")


def lookup_resolved_channel_helper(cls, channel_id: str) -> PartialChannel:
    return resolved_interactions_finder(cls, channel_id, "channels")


def lookup_resolved_user_helper(cls, user_id: str) -> User:
    return resolved_interactions_finder(cls, int(user_id), "users")


def lookup_resolved_role_helper(cls, role_id: str) -> Role:
    return resolved_interactions_finder(cls, int(role_id), "roles")