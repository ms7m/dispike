# Migration Guide (<1.0.0b)
***

v1.0.0b introduced a large number of breaking changes. 

- Renamed ``dispike.register`` to ``dispike.creating``.
- Moved ``allow_mentions`` file from ``dispike.models`` to ``dispike.creating``
- Moved ``components`` from ``dispike.helper`` to ``dispike.creating``
- Renamed ``dispike.models`` to ``dispike.incoming``
- Renamed ``incoming`` in ``dispike.incoming`` to ``incoming_interactions``
- ``bot.interactions.on`` has been deprecated. Please use ``bot.on`` instead or ``dispike.interactions.on``.
- ``EventHandler`` class has been removed, most of the functions have been implemented inside ``Dispike``
- The following commands now will raise an ``DiscordAPIError`` if the Discord API returns an unexpected status code. 
  - ``set_command_permission``
  - ``async_set_command_permission``
  - ``async_get_command_permission_in_guild``
  - ``async_get_all_command_permissions_in_guild``
  - ``get_all_command_permissions_in_guild``
  - ``get_command_permission_in_guild``
- Bot Tokens are no longer required to initialize a ``Dispike`` object.. Accessing methods, attributes or functions that require a bot token (such as registering commands) will now raise a new exception: ``dispike.errors.dispike.BotTokenNotProvided``. Certain features are still available without a bot token. Such as sending deferred messages or just responding to interactions. (closes #51) 
- DiscordResponse will now raise an exception ``dispike.errors.responses.InvalidDiscordResponse`` for certain combinations of values. (closes #50)
- Added ``default_permission`` to ``DiscordCommand``.. Learn more [here](https://discord.com/developers/docs/interactions/slash-commands#permissions). This value is set to ``True`` by default. (closes #53)

- Accessing methods such as ``.lookup_resolved_channel`` in ``IncomingDiscordInteraction`` with no resolved structures will now raise ``dispike.errors.response.NoResolvedInteractions``.

- ``CommandTypes`` has been changed to ``OptionTypes``. A new class of actual command types has been added. 
- ``IncomingDiscordOptionList`` changed to ``IncomingDiscordSlashData`` to better match what it actually is. 
- ``IncomingDiscordInteraction`` changed to ``IncomingDiscordSlashInteraction`` 
- ``DiscordCommand`` now takes a type which defaults to ``CommandTypes.SLASH`` (AKA Type 1) 
- ``DiscordCommand`` now validates that slash commands contain a description. 
- ``DiscordCommand`` now validates that context commands (Currently only ``MESSAGE``, ``USER``) do not have a description or options. 

- New events:  
    - ``MESSAGE_COMMAND``  
    - ``USER_COMMAND``

- New WIP classes ``Message`` and ``MessageAttachment``. Discord says they will add attachments as a option type in the future. 
- New ``IncomingInteraction`` ctx classes ``IncomingDiscordUserCommandInteraction`` and ``IncomingDiscordMessageCommandInteraction`` 