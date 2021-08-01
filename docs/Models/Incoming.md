# Incoming Objects

``IncomingDiscordInteraction`` is a helper object that is passed to *every* handler argument (``ctx``).

It allows you to view context from the command/button/menu from where it was sent and by who. It's recommended to read the [Discord documentation](https://discord.com/developers/docs/interactions/slash-commands#interaction-object) to learn more about what data is returned.

???+ info 
	If you want to change the keyword argument name in where the context will be passed to, you can pass ``custom_context_argument_name`` to ``Dispike``.


:::dispike.models.incoming