from pydantic import BaseModel, Field, ConfigDict


class Hotel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )
    id: int
    name: str
    city: str
    stars: int = Field(
        ge=1,
        le=5
    )
    latitude: float | None = Field(
        default=None,
        ge=-90,
        le=90
    )
    longitude: float | None = Field(
        default=None,
        ge=-180,
        le=180
    )