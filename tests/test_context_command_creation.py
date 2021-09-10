import pytest

from dispike.creating.models import *
from dispike.creating.models.options import CommandTypes
from dispike.interactions import PerCommandRegistrationSettings, EventCollection

user_expectation = {
    "name": "blep",
    "default_permission": True,
    "type": 2,
    "description": "",
    "options": [],
}

message_expectation = {
    "name": "blep",
    "default_permission": True,
    "type": 3,
    "description": "",
    "options": [],
}


def test_user_command_creation():
    command_to_create = DiscordCommand(
        name="blep",
        type=CommandTypes.USER,
    )

    # return command_to_create
    assert command_to_create.dict(exclude_none=True) == user_expectation


def test_message_command_creation():
    command_to_create = DiscordCommand(
        name="blep",
        type=CommandTypes.MESSAGE,
    )

    # return command_to_create
    assert command_to_create.dict(exclude_none=True) == message_expectation


def test_incorrect_command():
    with pytest.raises(ValueError):
        DiscordCommand(name="blep", type=CommandTypes.MESSAGE, description="!!")

    with pytest.raises(ValueError):
        DiscordCommand(name="blep", type=CommandTypes.SLASH, description="")
    
    with pytest.raises(ValueError):
        DiscordCommand(name="blep", type=CommandTypes.MESSAGE, description="!!", options=CommandOption(name="test", description="test", type=OptionTypes.BOOLEAN))
        