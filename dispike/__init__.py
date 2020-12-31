try:
    from importlib_metadata import version
except Exception:
    try:
        from importlib.metadata import version
    except Exception:

        def version(*args, **kwargs):
            return "unknown"


try:
    __version__ = version(__package__)
except Exception:
    __version__ = "unknown"

from .main import Dispike