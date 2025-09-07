from pydantic import BaseModel


class GmailAccountOut(BaseModel):
    account_id: str
    email: str
    status: str = "connected"

    class Config:
        from_attributes = True