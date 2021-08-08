import typing
from ..discord_types.member import PartialMember
from loguru import logger

if typing.TYPE_CHECKING:
    from ..incoming_interactions import IncomingDiscordInteraction


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

    _class_return = {
        "members": PartialMember,
    }
    try:
        _grab_member = cls.data.resolved["members"].get(query, None)
        if _grab_member is not None:
            return _class_return[type_to_determine](**_grab_member)
        return _grab_member
    except Exception:
        logger.exception(f"Unable to find query: {query} in resolved interactions..")


def lookup_resolved_member_helper(cls, member_id: str) -> PartialMember:
    return resolved_interactions_finder(cls, member_id, "members")
