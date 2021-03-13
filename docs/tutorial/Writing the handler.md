## Writing your first handler.

You’ve created and registered your first command.
Let’s write the handler so it can properly display to the user.

It’s a standard function with a few requirements.

- It must be async (``async def``)
- It must finally return: ``DiscordResponse``, or a ``dict``.

???+ warning
	If you return a ``dict``, it will not be verified and Dispike will assume that’s valid and return the result to Discord.


Your function must accept the same number of arguments you registered with Discord + an incoming context parameter.

Dispike will pass the same arguments (with the same names) to your function + incoming context about the request.

So if you registered a command with an argument named ``person``, the function argument must be the same.

???+ warning
	Rule of thumb, do not name arguments you are unable to name in standard python

## Incoming Context
Earlier you learned that you must account for an extra argument due to Dispike also passing a context about the command to your argument.

Incoming context is type hinted, and your IDE should be able to auto-complete attributes.


## Writing your function

```python

from discord.models.incoming IncomingDiscordInteraction

bot = Dispike(…)


@bot.interaction.on("wave")
async def handle_send_wave(person: int, ctx: IncomingDiscordInteraction) -> DiscordResponse:
  print(“recieved wave command”)
  

  # this is what we will be returning. Let's edit it.
  response = DiscordResponse()
  response.content f"👋 Hi @<{person}>."
  
  return response
	



```

Take a look at ``@bot.interaction.on(‘wave’)``, you can see that the ``.on`` takes in the command name we registered earlier.

The function also accepts two arguments. Our registered argument is named “person”, as well as the context that we will be receiving.

Also take a look at ``-> DiscordResponse``, this is a type-hint,  this is optional, but it will make your requests faster, as Dispike would not have to guess what your response type is.
