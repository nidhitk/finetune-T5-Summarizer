from pydantic import BaseModel


class DialogueInput(BaseModel):
    dialogue: str
