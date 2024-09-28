from pydantic import BaseModel, Field, constr


class HospitalResponseSchema(BaseModel):
    id: int
    name: str
    address: str
    contactPhone: str = constr(min_length=11, max_length=20)
    rooms: list[dict | str] = Field(default=[])