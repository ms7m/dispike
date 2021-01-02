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
This library has not left alpha stage and will have bugs and issues. I ask of you to please remember this when opening issues or creating PRs.

This library does not fully match the entire slash commands API spec. Namely

  - [Create Followup Message](https://discord.com/developers/docs/interactions/slash-commands#create-followup-message)
  - [Edit Followup Message](https://discord.com/developers/docs/interactions/slash-commands#edit-followup-message)
  - [Delete Followup Message](https://discord.com/developers/docs/interactions/slash-commands#delete-followup-message)

This library assumes you will be building an **independent server** to recieve and send requests from/to Discord directly. This may cause higher bandwith usages and incur costs with your cloud provider. If you prefer to listen over the Discord gateway, you should follow the progress of Discord.py instead.

This library enables a middleware to verify and accept connections **only from Discord** per documentation. **Although Discord is trusted, you should operate this bot behind a [reverse proxy](https://www.cloudflare.com/learning/cdn/glossary/reverse-proxy/) such as Nginx or Caddy, because of this, the bot will only bind to localhost and accept local connections.** 

If you want to do local testing before creating a server, you can use free tools such as [ngrok](https://ngrok.com/). 



This library is **only tested** on python versions

- 3.9
- 3.8
- 3.7
- 3.6





