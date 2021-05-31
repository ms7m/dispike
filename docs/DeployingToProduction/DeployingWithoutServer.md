## Deploying Without A Reverse Proxy Server

???+ warning
    This is not recommended unless your cloud provider/deployment service provides this already.

### Sample Bot File

```python
from dispike import Dispike

bot = Dispike(...)
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
$ uvicorn file_containing_bot:bot.referenced_application --host 0.0.0.0 --port 443
<span style="color: green;">INFO</span>:     Uvicorn running on http://0.0.0.0:443 (Press CTRL+C to quit)
```
</div>

``.referenced_application`` is extremely important.


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


***

# Important notes
- You may need to bind to 443 -- as discord requires HTTPS.