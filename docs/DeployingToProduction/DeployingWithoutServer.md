## Deploying Without A Reverse Proxy Server

???+ warning
    This is not recommended unless your cloud provider/deployment service provides this already.

### Sample Bot File

```python
from dispike import Dispike

bot = Dispike(...)
```





# Running directly from the bot.

```python
from dispike import Dispike

bot = Dispike(...)

# Bind port to something higher if you run into problems with root.
bot.run(bind_to_ip_address="0.0.0.0", port=443)
```



## Running bot with Uvicorn


### Installing Uvicorn
<div class="termy">
```console
$ pip install uvicorn[standard]
---> 100%
```
</div>

### Running the bot on a specific port + allowing outside connections.
<div class="termy">
```console
$ uvicorn file_containing_bot:bot.referenced_application --host 0.0.0.0 --port 444 --ssl-keyfile=./key.pem --ssl-certfile=./cert.pem
<span style="color: green;">INFO</span>:     Uvicorn running on http://0.0.0.0:443 (Press CTRL+C to quit)
```
</div>

``.referenced_application`` is extremely important.

You may want to read [Uvicorn's documentation](https://www.uvicorn.org/deployment) for more keyword arguments or to deploy with Gunicorn instead.


## Running bot with Hypercorn
<div class="termy">
```console
$ pip install hypercorn
---> 100%
```
</div>

### Running the bot on a specific port + allowing outside connections.
<div class="termy">
```console
$ hypercorn file_containing_bot:bot.referenced_application --bind 0.0.0.0:443
Running on 0.0.0.0:8080 over http (CTRL + C to quit)
```
</div>

``.referenced_application`` is extremely important.

