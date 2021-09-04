# Deploying with Reverse Proxy.



There may be some example configurations for your reverse proxy available [here](https://github.com/ms7m/dispike-example-server-configurations).



## Creating your configuration (Nginx)

### Run the bot with Uvicorn and bind to a UNIX socket.

<div class="termy">
```console
$ uvicorn file_containing_bot:bot.referenced_application --bind=unix:/tmp/dispike.sock
<span style="color: green;">INFO</span>:     Uvicorn running on unix:/tmp/dispike.sock (Press CTRL+C to quit)
```
</div>



??? info
	[Unix sockets are often twice as fast compared to using TCP ports](https://lists.freebsd.org/pipermail/freebsd-performance/2005-February/001143.html). Dispike allows you to bind to a local port (without binding to 0.0.0.0).

### Create your Nginx configuration. (This is a sample)

```nginx
worker_processes 1;

user nobody nogroup;
# 'user nobody nobody;' for systems with 'nobody' as a group instead
error_log  /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
  worker_connections 1024; # increase if you have lots of clients
  accept_mutex off; # set to 'on' if nginx worker_processes > 1
  # 'use epoll;' to enable for Linux 2.6+
  # 'use kqueue;' to enable for FreeBSD, OSX
}

http {
  include mime.types;
  # fallback in case we can't determine a type
  default_type application/octet-stream;
  access_log /var/log/nginx/access.log combined;
  sendfile on;

  upstream dispike {
    # fail_timeout=0 means we always retry an upstream even if it failed
    # to return a good HTTP response

    # for UNIX domain socket setups
    server unix:/tmp/dispike.sock fail_timeout=0;

    # for a TCP configuration
    # server 192.168.0.7:8000 fail_timeout=0;
  }

  server {
    # if no Host match, close the connection to prevent host spoofing
    listen 80 default_server;
    return 444;
  }

  server {
    # use 'listen 80 deferred;' for Linux
    # use 'listen 80 accept_filter=httpready;' for FreeBSD
    listen 443;
    client_max_body_size 4G;
    ssl_certificate /path/to/ssl/certificate;
    ssl_certificate_key /path/to/ssl/certificate/key;
    # set the correct host(s) for your site
    server_name example.com www.example.com;

    keepalive_timeout 5;


    location / {
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Proto $scheme;
      proxy_set_header Host $http_host;
      # we don't want nginx trying to do something clever with
      # redirects, we set the Host: header above already.
      proxy_redirect off;
      proxy_pass http://dispike;
    }

  }
}

```

If this doesn't work for you.. [DigitalOcean provides a tool to help you create a Nginx Configuration.](https://www.digitalocean.com/community/tools/nginx)



???+ info
	We have a WIP repository containing sample configurations for different proxies. Check it out [here](https://github.com/ms7m/dispike-example-server-configurations)

***

# Resources

Here are some resources to help you create configurations for your favorite reverse proxy server.

- https://fastapi.tiangolo.com/advanced/behind-a-proxy/
- [Caddy 2 Reverse Proxy](https://caddyserver.com/docs/) 
  - Caddy offers a functionality to automatically provision SSL certificates.





Once you are completed, start your proxy, configure DNS, and check if it's working by visiting ``https://your-server.com/ping``. 

