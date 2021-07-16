<p align="center">
	<a href="https://dispike.ms7m.me"><img src="./images/logo-frame.png" alt="Dispike"></a>
</p>
<p align="center">
		<em>Python library for building bots to interact with Discord Slash Commands</em>
</p>


<p align="center">

<a href="https://codecov.io/gh/ms7m/dispike" target="_blank">
		<img src="https://codecov.io/gh/ms7m/dispike/branch/master/graph/badge.svg?token=E5AXLZDP9O" alt="Test">
</a>

<a href="https://github.com/ms7m/dispike/actions" target="_blank">
		<img src="https://github.com/ms7m/dispike/workflows/Test%20Dispike/badge.svg?branch=master" alt="Coverage">
</a>

<a href="https://pypi.org/project/dispike" target="_blank">
		<img src="https://img.shields.io/badge/dynamic/json?color=blue&label=PyPi%20Version&query=%24.info.version&url=https%3A%2F%2Fpypi.org%2Fpypi%2Fdispike%2Fjson" alt="Package version">
</a>

</p>


# Before we start.
This library has not left the alpha stage and will have bugs and issues. I ask you to please remember this when opening issues or creating PRs.

This library assumes you will be building an **independent server** to receive and send requests from/to Discord directly. This may cause higher bandwidth usages and incur costs with your cloud provider. If you prefer to listen over the Discord gateway, you should follow the progress of Discord.py instead.

This library enables middleware to verify and accept connections **only from Discord** per documentation. **Although Discord is trusted, you should operate this bot behind a [reverse proxy](https://www.cloudflare.com/learning/cdn/glossary/reverse-proxy/) such as Nginx or Caddy, because of this, the bot will only bind to localhost and accept local connections.** 

If you want to do local testing before creating a server, you can use free tools such as [Ngrok](https://ngrok.com/). 



This library is **only tested** on python versions

- 3.9
- 3.8
- 3.7
- 3.6


***

# API Parity List
???+ info
	Just because it's been implemented does not mean it's in the best way. Help out by contributing to this library!

| API Endpoint   |      Implementation   |
|----------|:-------------:|
| Get Global Application Commands |  **✅ Implemented** |
| Create Global Application Command |    **✅ Implemented**   |
| Edit Global Application Command |  **✅ Implemented** |
| Delete Global Application Command | **✅ Implemented** |
| Create Guild Application Command | **✅ Implemented** |
| Edit Guild Application Command | **✅ Implemented** |
| Delete Guild Application Command | **✅ Implemented** |
| Create Interaction Response | **✅ Implemented** |
| Edit Original Interaction Response | **✅ Implemented**|
| Delete Original Interaction Response | **✅ Implemented** |
| Create Followup Message |**✅ Implemented** |
| Edit Followup Message | **✅ Implemented** |
| Delete Followup Message | **✅ Implemented** |
| Data Models and Types | **✅ Implemented** |
| ApplicationCommand | **✅ Implemented** |
| ApplicationCommandOption | **✅ Implemented** |
| ApplicationCommandOptionType | **✅ Implemented** |
| ApplicationCommandOptionChoice | **✅ Implemented** |
| Interaction | **✅ Implemented** |
| Interaction Response | **✅ Implemented** |
| Message Components | **✅ Implemented** |
| Buttons (Message Components) | **✅ Implemented** |
| Action Rows (Message Components) | **✅ Implemented** |
| Message Select (Message Components) | **✅ Implemented** |

[^1]: Message select is currently being tested and is not available..
### Special Thanks
- [Squidtoon99](https://github.com/Squidtoon99)
- [marshmallows](https://github.com/mrshmllow)
