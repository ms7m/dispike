from ..models.incoming import (
    IncomingDiscordInteraction,
    IncomingDiscordOptionList,
    SubcommandIncomingDiscordOptionList,
    IncomingDiscordOption,
)
import typing
from loguru import logger


def determine_event_information(
    interaction: IncomingDiscordInteraction,
) -> typing.Tuple[str, dict]:

    if isinstance(interaction, IncomingDiscordInteraction) == True:
        if (
            isinstance(interaction.data.options[0], SubcommandIncomingDiscordOptionList)
            == True
        ):
            # subcommand event names will be must be xxx.xxx
            _sub_command_arguments = {}
            _event_name = f"{interaction.data.name}.{interaction.data.options[0].name}"
            for argument in interaction.data.options[0].options:
                _sub_command_arguments[argument.name] = argument.value

            return _event_name, _sub_command_arguments

        elif isinstance(interaction.data.options[0], IncomingDiscordOption) == True:
            _command_arguments = {}

            for argument in interaction.data.options:
                argument: IncomingDiscordOption
                _command_arguments[argument.name] = argument.value

            return interaction.data.name, _command_arguments
    raise TypeError("unable to determine eventname.")