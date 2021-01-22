

# Dispike

Initalizing Dispike will require
    - A valid client public key
    - A valid bot token
    - A valid client id (Dispike references this as an application id.)

All of these values can be found in the Discord Developer Portal.
***

## Run command

The run method is available as a convenience to quickly start an HTTP server that can accept connections.
While this HTTP server itself is production-ready, you should run this behind a reverse-proxy such as Nginx :star:, Apache or Caddy.

The run method **will only bind to a local connection** and over a non-standard HTTP port.


:star: - *Recommended*

***

# Dispike Reference

:::dispike.Dispike

