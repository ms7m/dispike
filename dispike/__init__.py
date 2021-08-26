__version__ = "1.0.1-beta.0"

from .main import Dispike
from .incoming import IncomingDiscordSlashInteraction, IncomingApplicationCommand
from .response import DiscordResponse
from .creating.models import DiscordCommand
from .interactions import PerCommandRegistrationSettings, EventCollection

from loguru import logger

_add_networking_logging_level = logger.level("NETWORK", no=20, color="<fg #C954E2>")
