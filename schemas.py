from typing import List
from models import PropertyModel
from pydantic import BaseModel

class PropertyResponseModel(BaseModel):
    properties: List[PropertyModel]
