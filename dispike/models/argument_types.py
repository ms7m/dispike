
from pydantic import BaseModel, ValidationError, validator
import typing

try:
    from typing import Literal
except ImportError:
    # backport
    from typing_extensions import Literal


class ApplicationCommandInteractionData:
    incoming_id: int
    incoming_name: str
    incoming_options: typing.List[dict]

class TargetedUser(BaseModel):
    pass

class TargetedChannel(BaseModel):
    pass

class TargetedRole(BaseModel):
    pass

class TargetedString(BaseModel):
    pass

class TargetedInterger(BaseModel):
    pass

class TargetedBoolean(BaseModel):
    pass
