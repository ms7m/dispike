from dispike.incoming import (
    IncomingDiscordSlashInteraction,
    IncomingDiscordSlashData,
    SubcommandIncomingDiscordOptionList,
    IncomingDiscordOption,
    SubcommandIncomingDiscordOptionListChild,
)
import typing
from loguru import logger


def determine_event_information(
    interaction: IncomingDiscordSlashInteraction,
) -> typing.Tuple[str, dict]:

    if isinstance(interaction, IncomingDiscordSlashInteraction):

        if interaction.data.options is None:
            return interaction.data.name, {}

        if isinstance(interaction.data.options[0], SubcommandIncomingDiscordOptionList):
            # subcommand event names will be must be xxx.xxx
            _sub_command_arguments = {}

            if hasattr(interaction.data.options[0], "options"):
                # gosh this is hella ugly, i need to rewrite this.
                _event_name = (
                    f"{interaction.data.name}.{interaction.data.options[0].name}"
                )
                if isinstance(
                    interaction.data.options[0].options[0],
                    SubcommandIncomingDiscordOptionListChild,
                ):
                    _event_name += "." + interaction.data.options[0].options[0].name
            # I don't think below will ever happen, but just in case.
            else:  # pragma: no cover
                _event_name = (
                    f"{interaction.data.name}.{interaction.data.options[0].name}"
                )
            for argument in interaction.data.options[0].options:

                if isinstance(argument, SubcommandIncomingDiscordOptionListChild):
                    for sub_child_argument in argument.options:
                        _sub_command_arguments[
                            sub_child_argument.name
                        ] = sub_child_argument.value
                    break
                else:
                    _sub_command_arguments[argument.name] = argument.value

            return _event_name, _sub_command_arguments

        elif isinstance(interaction.data.options[0], IncomingDiscordOption):
            _command_arguments = {}

            for argument in interaction.data.options:
                argument: IncomingDiscordOption
                _command_arguments[argument.name] = argument.value

            return interaction.data.name, _command_arguments

    raise TypeError("unable to determine eventname.")
