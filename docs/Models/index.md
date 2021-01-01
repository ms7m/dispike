# Models

Models are responses or requests to and from discord that has been verified. Data can be accessed in a pythonic way of attrbiutes rather then dictionaries.

???+ info

	If you want a more low-level or want to transport models (pickling) you can access attributes ``.to_dict`` or ``.to_json``.



Models have been split into sections.

	- Incoming
	- Outgoing



Outgoing models are usually created by the user and and meant to be sent to discord, and have the strictest validation. They are easily editable by property.



Incoming models are usually models that have been translated from Discord themselves, and have been validated. While it's possible to edit the attributes, **no function** provided by Dispike will accept them. Treat them as read-only.



???+ info
	in certain circumstances, you can convert Incoming models to Outgoing, simply pass ``.to_dict`` of the incoming object to the appropriate outgoing object by doing ``OutgoingObject(**IncomingObject)``.


