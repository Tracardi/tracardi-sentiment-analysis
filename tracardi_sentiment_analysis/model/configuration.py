from pydantic import BaseModel, validator
from tracardi.domain.entity import Entity


class Configuration(BaseModel):
    source: Entity
    language: str = 'en'
    text: str

    @validator("language")
    def correct_lang(cls, value):
        langs = ["en", "sp", "fr", "it", "pt", "ct"]
        if value not in langs:
            raise ValueError("Incorrect language. Allowed values {}".format(langs))
        return value
