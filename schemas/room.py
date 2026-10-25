from pydantic import BaseModel, Field, ConfigDict


class Room(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )
    id: int
    hotelId: int
    pricePerNight: float = Field(
        ge=0
    )
    roomNumber: str
    guestsCount: int = Field(
        ge=1
    )