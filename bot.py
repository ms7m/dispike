from dispike.models.incoming import IncomingDiscordInteraction
from fastapi import FastAPI
from dispike.server import router, DiscordVerificationMiddleware, interaction
from loguru import logger


from dispike.response import DiscordStringResponse

app = FastAPI()
app.add_middleware(DiscordVerificationMiddleware, client_public_key="c0c4724137e3f18d09c70d7e0756045178261b7c419367c34c953c5108ca5149")
app.include_router(router)


@interaction.on("sendmessage")
async def testing(payload: IncomingDiscordInteraction):
    logger.info("Emitted.")
    #logger.info(payload.to_json())


    logger.debug(payload.member.user.id)
    logger.debug(payload.member.roles)

    _response = DiscordStringResponse()
    _response.content = f"Hello, {payload.member.user.username}!"
    

    return _response.response
