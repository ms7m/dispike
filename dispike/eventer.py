import typing
from fastapi import Response
from loguru import logger
import inspect

from functools import wraps


class EventHandler(object):
    def __init__(self):
        self.callbacks = {}

    def on(self, event, func=None):
        def on(func):
            if not inspect.iscoroutinefunction(func):
                raise TypeError("Function must be a async function.")

            if event not in self.callbacks:
                logger.debug(f"Added {event} to corresponding function to {func}")
                self.callbacks[event] = func
            else:
                raise TypeError("Events can only have one corresponding handler.")

            return func

        return on(func) if func else on

    def check_event_exists(self, event):
        return event in self.callbacks

    async def emit(self, event, *args, **kwargs):
        if event not in self.callbacks:
            raise TypeError(f"event {event} does not have a corresponding handler.")
        return await self.callbacks[event](**kwargs)
