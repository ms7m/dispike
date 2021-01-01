# Responses

Responses are what are returned to Discord. Either immediately or later.

## Immediate Responses

These responses are immediately returned after a request is received. 

To create a proper response, you will need the DiscordResponse object. 

## Responses For Later

If your request requires a request to be sent later (such as a long computational value.) You can simply return a NotReadyResponse. 

Provided with the bot instance, and a ``IncomingDiscordInteraction`` (which is the context in your handler.), it will provide methods for you to easily send your response when you are ready.

???+ warning
	The token to send the response expires after 15 minutes.
	




​	