## Ready Response

The ``DiscordResponse`` is available as a convenience object to assist you in generating a proper payload to return to discord. 

Some methods and functions may require you to *only* use a valid ``DiscordResponse``. 

```python
from dispike import DiscordResponse

# or

from dispike.responses import DiscordResponse

```

``content``, ``embeds``, and ``tts`` is not required immediately, and can be configured later.

However, settings such as ``show_user_input`` and ``follow_up_message`` are set at first initialization and cannot be changed.  


```python
from dispike.responses import DiscordResponse

response = DiscordResponse()
response.content = "Content Text Here"
```

```python
from dispike.responses import DiscordResponse
from dispike.helper import Embed
async def sample_function(...) -> DiscordResponse:
    ...
    return DiscordResponse(
        content="Content Text Here",
        tts=False,
        embeds=[Embed(...), Embed(...)],
        show_user_input=True
    )
```


### Empherical Messages
Empherical messages (messages/responses that are only visible to the person who sent them ) are available by setting the optional ``empherical`` parameter to ``True``. 

???+ info
    Setting a response to be empherical *after* initialization can be done by setting the ``._is_empherical`` attribute. (Note this will be changed in newer versions of Dispike.)

```python
from dispike.responses import DiscordResponse

response = DiscordResponse(empherical=True)
response.content = "Content Text Here"
```

![GifOfDeferredMessage](images/EmphericalMessageExample.png)



### Update original message

???+ warning
    You can only update an original message if you are responding to a component interaction

You can update the original message if you are responding to a component interaction.

```python
from dispike.responses import DiscordResponse

response = DiscordResponse(update_message=True)
response.content = "Brand new content"
```

### Buttons

???+ info
    Remember to register an event for these buttons!

```python
DiscordResponse(
    content="Content!",
    empherical=True,
    action_row=ActionRow(
        components=[
            Button(
                label="Next",
                custom_id="tutorial_step1_next",
                style=ButtonStyles.PRIMARY,
            ),
            Button(
                label="Cancel",
                custom_id="tutorial_cancel",
                style=ButtonStyles.DANGER,
            ),
            LinkButton(
                label="Go to the docs!",
                url="https://dispike.ms7m.me/"
            )
        ]
    ),
),
```

### Select Menus

???+ info
    Remember to register an event for this select menu!

```python
DiscordResponse(
    content="Content!",
    action_row=ActionRow(
        components=[
            SelectMenu(
                custom_id="class_select_1",
                placeholder="Choose a class",
                min_values=1,
                max_values=1,
                options=[
                    SelectMenu.SelectMenuOption(
                        label="Rogue",
                        description="Sneak n stab",
                        value="rogue",
                        emoji=PartialEmoji(name="rogue", id="625891304148303894"),
                    ),
                    SelectMenu.SelectMenuOption(
                        label="Mage",
                        description="Turn 'em into a sheep",
                        value="mage",
                        emoji=PartialEmoji(name="mage", id="625891304081063986"),
                    ),
                ],
                disabled=False,
            )
        ]
    ),
),
```


???+ info
    DiscordResponse is simply a helper to help you generate a valid response to discord. If you can generate a valid response yourself, you can simply type-hint your function to hint at a dict and return a *proper* response. This is only recommended for **Advanced** users.

:::dispike.response.DiscordResponse
