from pydantic import BaseModel
from tracardi.domain.entity import Entity


class Configuration(BaseModel):
    source: Entity
    language: str = 'en'
    text: str
