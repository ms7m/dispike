# Registering Collection

If you created a collection in a different file, you'll will need to register it with dispike.

???+ warning
	If your event collection needs to be initialized, do it before passing it to dispike. Otherwise, dispike can initialize it for you.. Passing your arguments to ``initialization_arguments`` and let dispike know to initialize it by passing ``initialze_on_load`` to ``register_collection`` function.



```python
from .other_file import SampleCollection
from dispike import Dispike


bot = Dispike(...)

bot.register_collection(
    collection=StockTicker,
    register_command_with_discord=True, # This parameter is optional.
)
```

``.register_collection`` will automatically detect any event callbacks with the ``interactions.on`` decorator.

