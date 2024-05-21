#!/usr/bin/python3
"""creates a Review class"""

from models.base_model import BaseModel

class Review(BaseModel):
    """managing review objects"""

    place_id = ""
    user_id = ""
    text = ""
