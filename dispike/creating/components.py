import typing
from enum import Enum

from pydantic import BaseModel

from dispike.errors.components import (
    InvalidComponentError,
    ComponentCombinationError,
    SelectMenuOptionError,
)


class ComponentTypes(int, Enum):

    """Easy access to component types.

    Attributes:
        ACTION_ROW (int): Represents Type 1
        BUTTON (int): Represents Type 2
        SELECT_MENU (int): Represents Type 3
    """

    ACTION_ROW = 1
    BUTTON = 2
    SELECT_MENU = 3


class ButtonStyles(int, Enum):

    """Easy access to button styles.

    Attributes:
        PRIMARY (int): Represents Style 1
        SECONDARY (int): Represents Style 2
        SUCCESS (int): Represents Style 3
        DANGER (int): Represents Style 4
        LINK (int): Represents Style 5
    """

    PRIMARY = 1
    SECONDARY = 2
    SUCCESS = 3
    DANGER = 4
    LINK = 5


class PartialEmoji:
    """Represents a partial Discord emoji"""

    def __init__(self, name: str, id: str = None, animated: bool = None):
        """
        Args:
            name (str): The emojis name, or unicode symbol.
            id (str, optional): id of the emoji, if not a unicode one.
            animated (bool, options): bool Specifying if this emoji should be animated, if not a unicode one.
        """
        self.name = name
        self.id = id
        self.animated = animated

    def to_dict(self):
        _dict = {"name": self.name}
        if self.id:
            _dict["id"] = self.id
        if self.animated is not None:
            _dict["aniamted"] = self.animated
        return _dict


class Button:
    """Represents a partial Discord emoji"""

    def __init__(
        self,
        label: str = None,
        custom_id: str = None,
        disabled: bool = False,
        style: ButtonStyles = ButtonStyles.PRIMARY,
        emoji: PartialEmoji = None,
    ):
        """
        Args:
            label (str): label of the button.
            custom_id (str, optional): custom id of the button.
            disabled (bool, optional): bool specifying if this button should be disabled.
            style (ButtonStyles, optional): style of the button. Cannot be LINK
            emoji (PartialEmoji, optional): a partial emoji.
        """
        self.type = ComponentTypes.BUTTON

        if style == ButtonStyles.LINK:
            raise TypeError("style cannot be type Link")
        if not label:
            raise TypeError("label cannot be None")
        if not custom_id:
            raise TypeError("custom_id cannot be None")

        self.style = style
        self.label = label
        self.custom_id = custom_id
        self.disabled = disabled
        self.emoji = emoji

    def to_dict(self):
        temp_dict = {
            "type": self.type.value,
            "style": self.style.value,
            "label": self.label,
            "custom_id": self.custom_id,
        }

        # an emoji is optional
        if self.emoji:
            temp_dict["emoji"] = self.emoji.to_dict()

        return temp_dict


class LinkButton:
    """Represents a partial Discord emoji"""

    def __init__(self, label: str = None, url: str = None, disabled: bool = False):
        """
        Args:
            label (str): Label of the button.
            url (str): Url of the link button.
            disabled (bool, optional): bool Specifying if this button should be disabled.
        """
        self.type = ComponentTypes.BUTTON
        self.style = ButtonStyles.LINK

        if not url:
            raise TypeError("url cannot be None")
        if not label:
            raise TypeError("label cannot be None")

        self.label = label
        self.url = url
        self.disabled = disabled

    def to_dict(self):
        return {
            "type": self.type.value,
            "style": self.style.value,
            "label": self.label,
            "url": self.url,
            "disabled": self.disabled,
        }


class SelectMenu:
    """Represents a Discord select menu"""

    class SelectMenuOption:
        """Represents a Discord select menu option"""

        def __init__(
            self,
            label: str = None,
            value: str = None,
            description: str = None,
            emoji: PartialEmoji = None,
            default: bool = False,
        ):
            """
            Args:
                label (str): Label of the option.
                value (str): Internal value of the option.
                description (str): Description of the option.
                emoji (PartialEmoji, optional): A partial emoji
                default (bool): Whether or not this option should be the default.
            """

            if not label:
                raise TypeError("label cannot be None")
            if not value:
                raise TypeError("value cannot be None")

            self.label = label
            self.value = value
            self.description = description
            self.emoji = emoji
            self.default = default

        def to_dict(self):
            temp_dict = {
                "label": self.label,
                "value": self.value,
                "default": self.default,
            }

            if self.description:
                temp_dict["description"] = self.description
            if self.emoji:
                temp_dict["emoji"] = self.emoji.to_dict()

            return temp_dict

    def __init__(
        self,
        custom_id: str,
        options: typing.List[SelectMenuOption],
        placeholder: str,
        min_values: int,
        max_values: int,
        disabled: False,
    ):
        """
        Args:
            custom_id (str): Custom id of the menu.
            options (SelectMenu.SelectMenuOption): List of SelectMenu.SelectMenuOption's
            placeholder (str, optional): Text that's shown before a user selects anything.
            min_values (int): The minimum amount of values a user can select. Cannot be lower than 0
            max_values (int): The maximum amount of values a user can select. Cannot be higher than the amount of options.
            disabled (bool, optional): Whether to disable menu
        """
        self.type = ComponentTypes.SELECT_MENU
        self.options = options

        for option in options:
            if not isinstance(option, SelectMenu.SelectMenuOption):
                raise SelectMenuOptionError(f"{option} is not type SelectMenuOption")

        if not placeholder:
            raise TypeError("placeholder cannot be None")
        if not custom_id:
            raise TypeError("custom_id cannot be None")

        self.placeholder = placeholder
        self.custom_id = custom_id

        if not min_values or not max_values:
            raise TypeError("min_values or max_values must not be None")

        if max_values > len(options):
            raise TypeError(
                "max_values cannot be larger than how many options you have"
            )
        if min_values < 1:
            raise TypeError("min_values cannot be less than 0")

        self.min_values = min_values
        self.max_values = max_values

        self.disabled = disabled

    def to_dict(self):
        return {
            "type": self.type.value,
            "options": [x.to_dict() for x in self.options],
            "custom_id": self.custom_id,
            "min_values": self.min_values,
            "max_values": self.max_values,
            "placeholder": self.placeholder,
            "disabled": self.disabled,
        }




class ActionRow:
    """Represents a action row component"""

    def __init__(
        self, components: typing.List[typing.Union[Button, LinkButton, SelectMenu]]
    ):
        """
        Args:
            components (typing.List[typing.Union[Button, LinkButton, SelectMenu]]): Components for this action row. You cannot combine buttons and select menus
        """

        self.type = ComponentTypes.ACTION_ROW

        # Do a heap of stuff to figure out if a select menu is being combined with a button
        contains_button = False
        contains_select_menu = False
        for component in components:
            if isinstance(component, (Button, LinkButton)):
                contains_button = True
            elif isinstance(component, SelectMenu):
                contains_select_menu = True
            else:
                # raise error if neither.
                raise InvalidComponentError(type(component))

        if contains_button and contains_select_menu:
            raise ComponentCombinationError(
                "You cannot combine buttons and select menus"
            )

        self.components = components

    def to_dict(self):
        return {
            "type": self.type.value,
            "components": [x.to_dict() for x in self.components],
        }

    def __eq__(self, other: "ActionRow"):
        return (
            self.__dict__ == other.__dict__
            and [x.to_dict() for x in self.components]
            == [x.to_dict() for x in self.components]
            and self.__class__ == other.__class__
        )
