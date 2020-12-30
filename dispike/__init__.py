from importlib_metadata import version

try:
    __version__ = version(__package__)
except Exception:
    __version__ = "unknown"

from .main import Dispike