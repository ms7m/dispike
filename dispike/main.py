from fastapi import FastAPI
from loguru import logger
from .server import router, DiscordVerificationMiddleware
from .server import interaction as router_interaction

import uvicorn

class Dispike(object):
    def __init__(self, client_public_key: str):
        self._internal_application = FastAPI()
        self._internal_application.add_middleware(
            DiscordVerificationMiddleware,
            client_public_key=client_public_key
        )
        self._internal_application.include_router(
            router=router
        )

    @property
    def interaction(self):
        return router_interaction

    @property
    def referenced_application(self):
        return self._internal_application
    
    def run(self, port: int = 5000):
        uvicorn.run(app=self.referenced_application, port=port)