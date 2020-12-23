from pydantic import BaseModel

try:
    from typing import Literal
except ImportError:
    # backport
    from typing_extensions import Literal


class User(BaseModel):
    class Config:
        arbitary_types_allowed = True

    id: int
    username: str
    avatar: str
    discriminator: str
    public_flags: int
