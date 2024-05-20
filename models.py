from pydantic import BaseModel, Field
from typing import Optional

class PropertyModel(BaseModel):
    name: str = Field(...)
    address: str = Field(...)
    city: str = Field(...)
    state: str = Field(...)

class UpdatePropertyModel(BaseModel):
    name: Optional[str]
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
