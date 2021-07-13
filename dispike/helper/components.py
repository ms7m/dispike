import typing
from enum import Enum


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
    def __init__(self, name: str = None, id: str = None, animated: bool = None):
        if not name:
            raise TypeError("name cannot be None")

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
    def __init__(
        self,
        label: str = None,
        custom_id: str = None,
        disabled: bool = False,
        style: ButtonStyles = ButtonStyles.PRIMARY,
        emoji: PartialEmoji = None,
    ):
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
    def __init__(self, label: str = None, url: str = None, disabled: bool = False):
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
    class SelectMenuOption:
        def __init__(
            self,
            label: str = None,
            value: str = None,
            description: str = None,
            emoji: PartialEmoji = None,
            default: bool = False,
        ):
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
        self.type = ComponentTypes.SELECT_MENU
        self.options = options

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

    def to_dict(self):
        return {
            "type": self.type.value,
            "options": [x.to_dict() for x in self.options],
            "custom_id": self.custom_id,
            "min_values": self.min_values,
            "max_values": self.max_values,
            "placeholder": self.placeholder,
        }


class ActionRow:
    """Represents a action row component"""

    def __init__(
        self, components: typing.List[typing.Union[Button, LinkButton, SelectMenu]]
    ):
        self.type = ComponentTypes.ACTION_ROW

        # Do a heap of stuff to figure out if a select menu is being combined with a button
        contains_button = False
        contains_select_menu = False
        for component in components:
            if type(component) == Button or type(component) == LinkButton:
                contains_button = True
            elif type(component) == SelectMenu:
                contains_select_menu = True

        if contains_button and contains_select_menu:
            raise TypeError("You cannot combine buttons and select menus")

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
