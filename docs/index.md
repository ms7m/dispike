

<div align="center">
<p align="center">
	<a href="https://dispike.ms7m.me"><img src="./images/logo-frame.png" alt="Dispike"></a>
</p>
  <h1> dispike </h1>
  <i> ⚙️  A simple to use, powerful framework for creating stateless, independent bots using <a href="https://discord.com/developers/docs/interactions/slash-commands"> Discord Slash Commands.</a> </i>
  <br>
  <br>
    <a > ⚡ Powered by <a href="https://github.com/tiangolo/fastapi"> FastAPI.</a> </a>
  <br>
  <br>
  <p align="center">
    <img src="https://codecov.io/gh/ms7m/dispike/branch/master/graph/badge.svg?token=E5AXLZDP9O">
    <img src="https://github.com/ms7m/dispike/workflows/Test%20Dispike/badge.svg?branch=master">
    <img src="https://img.shields.io/badge/Available%20on%20PyPi-Dispike-blue?logo=pypi&link=%22https://pypi.org/project/dispike%22">
    <img src="https://img.shields.io/badge/dynamic/json?color=blue&label=PyPi%20Version&query=%24.info.version&url=https%3A%2F%2Fpypi.org%2Fpypi%2Fdispike%2Fjson">
  </p>
  <br>
</div>


# Before we start.
This library is currently in beta. While things are more stable than earlier releases, breaking changes can still be introduced. It's recommended to stay in the loop with the repository such as joining our Discord server for announcements.

This library assumes you will be building an **independent server** to receive and send requests from/to Discord directly. This may cause higher bandwidth usages and incur costs with your cloud provider. If you prefer to listen over the Discord gateway, you should follow the progress of Discord.py instead.

This library enables middleware to verify and accept connections **only from Discord** per documentation. **Although Discord is trusted, you should operate this bot behind a [reverse proxy](https://www.cloudflare.com/learning/cdn/glossary/reverse-proxy/) such as Nginx or Caddy, because of this**, or use a "serverless" platform such as Amazon Lambda (with an adapter) or Google Cloud App Engine.

If you want to do local testing before creating a server, you can use free tools such as [Ngrok](https://ngrok.com/). 



This library is **only tested** on python versions

- 3.9
- 3.8 ^*
- 3.7
- 3.6

[^*]: Coverage tested on this version of python.


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
- [marshmallow](https://github.com/mrshmllow)
