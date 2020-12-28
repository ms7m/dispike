from dispike.register.models.options import CommandChoice, CommandOption
from dispike.register.register import *

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
            "choices": [],
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
    assert command_to_create.dict() == expectation