from pydantic import BaseModel


class SASourceConfiguration(BaseModel):
    token: str
