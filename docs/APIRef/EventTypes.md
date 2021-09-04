# Event Types

Dispike comes with support for all forms of Discord Interactions.

| Event Name               | Enum                |   |   |
|--------------------------|---------------------|---|---|
| Commands                 | ``COMMAND``         |   |   |
| Components (i.e Buttons) | ``COMPONENT``       |   |   |
| Message Commands         | ``message_command`` |   |   |
| User Commands            | ``user_command``    |   |   |


You **must** pass an interaction type when adding the interaction decorator.  By default, we will pass the ``EventTypes.COMMAND`` interaction type.

