import typing_extensions, typing
from dispike.creating.models import permissions


class PermissionGenerator(object):
    """A helper that helps you create proper permissions for a slash command."""

    def __init__(
        self,
        restrict_to_role: bool = False,
        restrict_to_user: bool = False,
        restricted_role_id: typing.Union[list[int], int] = [],
        restricted_user_id: typing.Union[list[int], int] = [],
        allow_all_except_or_deny_all_except: typing.Union[
            typing_extensions.Literal["allow_all"],
            typing_extensions.Literal["deny_all"],
        ] = "allow_all",
    ):
        """A Helper that helps you create proper permissions for a slash command. Generates a NewApplicationPermission.

        Args:
            restrict_to_role (bool, optional): Whether to restrict to a specific Discord Role ID.. Defaults to False.
            restrict_to_user (bool, optional): Whether to restrict to a specific Discord User ID. Defaults to False.
            restricted_role_id (int, optional): The restricted role ID. Defaults to None.
            restricted_user_id (int, optional): The restricted user ID. Defaults to None.
            allow_all_except_or_deny_all_except (Union["allow_all", "deny_all"], optional): Whether to allow only X or allow everyone else other than X. Defaults to "allow_all".

        Raises:
            TypeError: If `allow_all_except_or_deny_all_except` is not a valid value.
            ValueError: If you attempt to combine restrictions.
        """

        self.__restrict_to_role = restrict_to_role
        self.__restrict_to_user = restrict_to_user

        if restrict_to_role == False:
            self.__restricted_role_id = []
        elif isinstance(restrict_to_role, int):
            self.__restricted_role_id = [restricted_role_id]
        elif isinstance(restrict_to_role, list):
            if restrict_to_role == []:
                self.__restricted_role_id = []
            else:
                for _item in restricted_role_id:
                    if isinstance(_item, int) == False:
                        raise ValueError(
                            f"Value passed to restricted roles is not a valid type. Recieved {type(restrict_to_role)}.. Need <int>!"
                        )
                self.__restricted_role_id = restricted_role_id
        else:
            raise TypeError(
                "Unknown type recieved for role.. If this is a string, go ahead and convert it to an int"
            )

        if restrict_to_user == False:
            self.__restricted_user_id = []
        elif isinstance(restrict_to_user, int):
            self.__restricted_user_id = [restricted_user_id]
        elif isinstance(restrict_to_user, list):
            if restricted_user_id == []:
                self.__restricted_user_id = []
            else:
                for _item in restricted_role_id:
                    if isinstance(_item, int) == False:
                        raise ValueError(
                            f"Value passed to restricted users is not a valid type. Recieved {type(restrict_to_user)}.. Need <int>!"
                        )
                self.__restricted_user_id = restricted_user_id
        else:
            raise TypeError(
                "Unknown type recieved for user.. If this is a string, go ahead and convert it to an int"
            )

        if allow_all_except_or_deny_all_except not in ["allow_all", "deny_all"]:
            raise TypeError(
                f"{allow_all_except_or_deny_all_except} is unknown. Cannot determine whether to deny or allow based on permission"
            )
        else:
            if allow_all_except_or_deny_all_except == "deny_all":
                self.__allow_all_except_or_deny_all_except = False
            else:
                self.__allow_all_except_or_deny_all_except = True

        if self.__restrict_to_role and self.__restricted_role_id is []:
            raise ValueError("Cannot restrict to role without a role id")

        if self.__restrict_to_user and self.__restricted_user_id is []:
            raise ValueError("Cannot restrict to user without a user id")

    @property
    def restricted_to_role(self) -> bool:
        return self.__restrict_to_role

    @property
    def restricted_to_user(self) -> bool:
        return self.__restrict_to_user

    @property
    def restricted_role_id(self) -> typing.List[int]:
        return self.__restricted_role_id

    @property
    def restricted_user_id(self) -> typing.List[int]:
        return self.__restricted_user_id

    @property
    def allow_all_except_or_deny_all_except(self) -> bool:
        return self.__allow_all_except_or_deny_all_except

    def remove_role_from_restricted_roles(self, role_id: int):
        if role_id in self.__restricted_role_id:
            self.__restricted_role_id.remove(role_id)

    def add_role_to_restricted_roles(
        self, role_id: int, ignore_if_already_present: bool = False
    ):
        if role_id in self.__restricted_role_id:
            if ignore_if_already_present:
                return
            else:
                raise ValueError(
                    f"Role {role_id} is already in the restricted roles. Cannot add it again."
                )
        else:
            self.__restricted_role_id.append(role_id)

    def remove_user_from_restricted_roles(self, user_id: int):
        if user_id in self.__restrict_to_user:
            self.__restrict_to_user.remove(user_id)

    def add_user_to_restricted_users(
        self, user_id: int, ignore_if_already_present: bool = False
    ):
        if user_id in self.__restrict_to_user:
            if ignore_if_already_present:
                return
            else:
                raise ValueError(
                    f"User {user_id} is already in the restricted users. Cannot add it again."
                )
        else:
            self.__restrict_to_user.append(user_id)

    @allow_all_except_or_deny_all_except.setter
    def set_allow_all_except_or_deny_all_except(self, new_value):
        if new_value not in ["allow_all", "deny_all"]:
            raise TypeError(
                f"{new_value} is unknown. Cannot determine whether to deny or allow based on permission"
            )
        else:
            if new_value == "deny_all":
                self.__allow_all_except_or_deny_all_except = False
            else:
                self.__allow_all_except_or_deny_all_except = True

    @property
    def created(self) -> permissions.NewApplicationPermission:
        """Returns a NewApplicationPermission object based on the current attributes.

        Returns:
            permissions.NewApplicationPermission: A properly configured object.
        """

        _permissions_generated = []
        if self.restricted_to_role:
            if self.__restricted_role_id == []:
                raise ValueError("Cannot create restriction for roles with no role ids")

            for role_to_restrict in self.restricted_role_id:
                _permissions_generated.append(
                    permissions.ApplicationCommandPermissions(
                        id=role_to_restrict,
                        type=permissions.ApplicationCommandPermissionType.ROLE,
                        permission=self.__allow_all_except_or_deny_all_except,
                    )
                )

        if self.restricted_to_user:
            if self.__restricted_user_id == []:
                raise ValueError("Cannot create restriction for roles with no role ids")

            for role_to_restrict in self.restricted_user_id:
                _permissions_generated.append(
                    permissions.ApplicationCommandPermissions(
                        id=role_to_restrict,
                        type=permissions.ApplicationCommandPermissionType.USER,
                        permission=self.__allow_all_except_or_deny_all_except,
                    )
                )

        return permissions.NewApplicationPermission(permissions=_permissions_generated)
