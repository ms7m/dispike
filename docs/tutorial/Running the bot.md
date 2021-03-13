## Running your bot.

Great, you successfully created, registered, and wrote a handler for a command.

We need to run the bot. 

???+ info
	It’s important to remember, when you are ready to deploy 	your bot, you will need to deploy your bot over a reverse 	proxy (which is beyond the scope of the docs.).
	

Now, since we don’t have a server set up yet, how are we going to test our bot? It’s a pain in the ass to have a server just for testing. Luckily there is a tool that can help us.

We’re going to use a tool called [ngrok](https://ngrok.com/). It creates a tunnel that is accessible over the internet to a local port running on your computer.

Sign-up and install ngrok.

### Start ngrok.

Open a new terminal window, and run
```
ngrok http 5000
```

Take a note at the HTTPS link, this is the link you will provide to discord.

???+ info
	If you try to give discord the link, it will fail. The bot is not running and nothing is there to run the first verification.

### Start the bot.

There are multiple ways to run the bot. We’re going to use the simplest one.

Add the following lines to the end of the file containing the bot object and handler

```python

if __name__ == “__main__”:
	bot.run(port=5000)
```

???+ warning
	This is simple, but is not meant for production!

Open your web-browser (or postman) and try to test if your bot is reachable by going to the link that ngrok has provided and appending ``/ping``

You should see a message telling you it’s reachable.

Afterwards, go to discord and add the interaction point url, with the url that ngrok has provided appended with /interactions

![ExampleInteraction](./images/ExampleEndpointEnter.png)

Press submit, and Discord will test your link by sending two requests, they should pass.



### Run some commands.

Congrats, if tests pass, invite your bot into a server, and try out some bot commands!


