from pydantic import BaseModel, ConfigDict


class TextMail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    mail_text: str
