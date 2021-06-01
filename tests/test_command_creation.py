from dispike.register import RegisterCommands
from dispike.register.models import *


expectation = {
    "name": "blep",
    "description": "Send a random adorable animal photo",
    "options": [
        {
            "name": "animal",
            "description": "The type of animal",
            "type": 3,
            "required": True,
            "choices": [
                {"name": "Dog", "value": "animal_dog"},
                {"name": "Cat", "value": "animal_cat"},
                {"name": "Penguin", "value": "animal_penguin"},
            ],
        },
        {
            "name": "only_smol",
            "description": "Whether to show only baby animals",
            "type": 5,
            "required": False,
        },
    ],
}


def test_command_creation():
    command_to_create = DiscordCommand(
        name="blep",
        description="Send a random adorable animal photo",
        options=[
            CommandOption(
                name="animal",
                description="The type of animal",
                type=3,
                required=True,
                choices=[
                    CommandChoice(name="Dog", value="animal_dog"),
                    CommandChoice(name="Cat", value="animal_cat"),
                    CommandChoice(name="Penguin", value="animal_penguin"),
                ],
            ),
            CommandOption(
                name="only_smol",
                description="Whether to show only baby animals",
                type=5,
                required=False,
            ),
        ],
    )

    # return command_to_create
    assert command_to_create.dict(exclude_none=True) == expectation


def test_mulitple_subcommands():
    command_to_create = DiscordCommand(
        **{
            "name": "testsubcommand",
            "description": "sample description for testing subcommands",
            "options": [
                {
                    "type": 1,
                    "name": "testsub1",
                    "description": "test inner subcommand",
                    "options": [],
                },
                {
                    "type": 1,
                    "name": "testsub2",
                    "description": "test inner subcommand 2",
                    "options": [],
                },
            ],
        }
    )
    assert command_to_create.name == "testsubcommand", "Unexpected command name"
    assert (
        command_to_create.description == "sample description for testing subcommands"
    ), "Unexpected command description"

    assert (
        command_to_create.options[0].name == "testsub1"
    ), "Unexpected subcommand 1 name"
    assert (
        command_to_create.options[1].name == "testsub2"
    ), "Unexpected subcommand 2 name"

    assert (
        command_to_create.options[0].description == "test inner subcommand"
    ), "Unexpected subcommand inner subcommand description"
    assert (
        command_to_create.options[1].description == "test inner subcommand 2"
    ), "Unexpected subcommand inner subcommand 2 description"


def test_subcommand_group():
    command_to_create = DiscordCommand(
        **{
            "name": "testsubcommand",
            "description": "sample description for testing subcommands",
            "options": [
                {
                    "type": 2,
                    "name": "subcommandgroup",
                    "description": "testing subcommandgroup",
                    "options": [
                        {
                            "type": 1,
                            "name": "innertest",
                            "description": "inner test 1",
                            "options": [],
                        }
                    ],
                }
            ],
        }
    )
    assert command_to_create.name == "testsubcommand"
    assert command_to_create.description == "sample description for testing subcommands"

    assert command_to_create.options[0].type == 2
    assert command_to_create.options[0].name == "subcommandgroup"
    assert command_to_create.options[0].description == "testing subcommandgroup"
    assert command_to_create.options[0].options[0].name == "innertest"
    assert command_to_create.options[0].options[0].type == 1
