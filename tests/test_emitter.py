
from dispike.eventer import EventHandler
import pytest
event_handler = EventHandler()


@event_handler.on("sampleEvent")
async def dummy_function(*args, **kwargs):
    return kwargs.get('payload')

@pytest.mark.asyncio
async def test_event_handler():
    assert await event_handler.emit('sampleEvent', payload=True) == True
    assert "sampleEvent" in event_handler.callbacks

def test_non_async_event_handler():
    with pytest.raises(TypeError):
        @event_handler.on("badEvent")
        def test_function(*args, **kwargs):
            return True
