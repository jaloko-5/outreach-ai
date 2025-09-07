from typing import List, Optional
from pydantic import BaseModel, EmailStr


class RecipientCreate(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company: Optional[str] = None
    custom_fields: Optional[dict] = None


class CampaignCreate(BaseModel):
    user_id: str
    sender_account_id: str
    name: str
    type: str = "cold_outreach"
    email_subject: str
    html_content: str = ""
    text_content: str = ""
    settings: Optional[dict] = None
    recipients: List[RecipientCreate] = []


class CampaignOut(BaseModel):
    id: str
    name: str
    status: str

    class Config:
        from_attributes = True