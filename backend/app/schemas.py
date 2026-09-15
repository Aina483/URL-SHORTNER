"""Pydantic schema for the request and response of the URL shortening"""
from pydantic import BaseModel, Field, ConfigDict, field_validator, HttpUrl

from datetime import datetime

class URLCreateRequest(BaseModel):
    """Payload for POST /api/urls."""

    original_url: str = Field(..., min_length=1, max_length=2048, examples=["https://example.com/a/long/path"])
    custom_code: str | None = Field(
            default=None,
            min_length=3,
            max_length=16,
            pattern=r"^[A-Za-z0-9_-]+$",
            description="Optional caller-chosen alias for the short code.",
        )

    @field_validator('orignal_url')
    @classmethod
    def validate_url(cls, value :str) -> str:
        try:
            HttpUrl(value)
        except Exception:
            raise ValueError("Invalid URL")

        return value

class URLResponse(BaseModel):
    """Response shape for a single shortened URL."""
    # from_attributes usgae and helpfulness: when your data comes from Python objects 
    # (especially database/ORM objects) rather than dictionaries.
    model_config = ConfigDict(from_attributes= True)
    id : int
    short_code : str
    short_url : str
    orignal_url : str
    click_count : int
    created_at : datetime

class URLListReponse(BaseModel):
    items : list[URLResponse]
    total : int
    limit : int
    offset : int



    
            
        
