#!/usr/bin/python3
"""creates a User class"""

from models.base_model import BaseModel

class City(BaseModel):
    """managing city objects"""

    state_id = ""
    name = ""
