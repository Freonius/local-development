# pylint: disable=no-name-in-module
from pydantic import BaseModel

# pylint: enable= no-name-in-module


class BasicResponse(BaseModel):
    """A basic response model"""

    message: str
