# Deferred Messages

Deferred Messages are messages that will appear later to the user. 
![GifOfDeferredMessage](images/loadingDeferred.gif)

***

## Setting up the handler.

Setting up the handler for deferred response commands are a little bit different compared to normal commands. Dispike will automatically run your handler function after responding to Discord.

???+ warning
	You have 15 Minutes to respond back to Discord before the token expires. 

Deferred Responses are useful for commands that require background processing that otherwise would lead to an error if it was a standard command.


### Requirements
Your handler **must** hint a return of ``DeferredResponse``. Any other hinted return (or no hinted return) may result in a delay in your bot responding. 

When you are ready to send your respond, use the provided function ``.send_deferred_message`` in your bot instance.

???+ warning
	Your handler must still be an async function!

***
```python
@bot.interaction.on("new.code")
async def generate_secret_code(ctx: IncomingDiscordInteraction) -> DeferredResponse:
    data = _heavy_function()
    # Compute-heavy task here.
    #
    # Remember that you have 15 minutes to respond before the token
    # expires..
    #
    await bot.send_deferred_message(
        original_context=ctx,
        new_message=DiscordResponse(content="back with a new response."),
    )
```

