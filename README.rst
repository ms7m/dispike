dispike
=======

--------------

|codecov| |Test Dispike| |PyPi Link| |PyPiVersion| |Docs|

--------------

an *extremely-extremely* early WIP library for easily creating
REST-based webhook bots for discord using the new Slash Commands
feature.

Powered by FastAPI.

--------------

Install
-------

::

   pip install dispike

Learn more
----------

-  Read documentation `here <https://dispike.ms7m.me>`__
-  See example bot
   `here <https://github.com/ms7m/dispike-example-bot>`__

Example Code
------------

.. code:: python


   from dispike import Dispike
   bot = Dispike(..)

   @bot.interaction.on("stock"):
   async def handle_stock_request(stockticker: str, ctx: IncomingDiscordInteraction) -> DiscordResponse:
     get_price = function(stockticker...)
     
     embed=discord.Embed()
     embed.add_field(name="Stock Price for {stockticker}.", value="Current price is {get_price}", inline=True)
     embed.set_footer(text="Request received by {ctx.member.user.username}")
     return DiscordResponse(embed=embed)

Caveats
-------

-  [STRIKEOUT:Does not handle registring new commands.]
-  [STRIKEOUT:Does not handle anything other then string responses.
   (However you are free to return any valid dict in your handler.)]
-  [STRIKEOUT:Not on PyPi]
-  Does not speak over the discord gateway. You’ll need a server to
   handle requests and responses.
-  Python 3.6+
-  [STRIKEOUT:Handling followup messages.]

Development
===========

Help is wanted in mantaining this library. Please try to direct PRs to
the ``dev`` branch, and use black formatting (if possible).

.. figure:: https://github.com/ms7m/dispike/workflows/Test%20Dispike/badge.svg?branch=dev
   :alt: Test Dispike

   Test Dispike

.. |codecov| image:: https://codecov.io/gh/ms7m/dispike/branch/master/graph/badge.svg?token=E5AXLZDP9O
   :target: https://codecov.io/gh/ms7m/dispike
.. |Test Dispike| image:: https://github.com/ms7m/dispike/workflows/Test%20Dispike/badge.svg?branch=master
.. |PyPi Link| image:: https://img.shields.io/badge/Available%20on%20PyPi-Dispike-blue?logo=pypi
   :target: https://pypi.org/project/dispike
.. |PyPiVersion| image:: https://img.shields.io/badge/dynamic/json?color=blue&label=PyPi%20Version&query=%24.info.version&url=https%3A%2F%2Fpypi.org%2Fpypi%2Fdispike%2Fjson
.. |Docs| image:: https://img.shields.io/badge/Docs-Available-lightgrey
   :target: https://dispike.ms7m.me/

