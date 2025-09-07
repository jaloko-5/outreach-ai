import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.session import get_db
from app.models.campaign import Campaign
from app.models.recipient import Recipient
from app.models.gmail_account import GmailAccount
from app.models.user import User
from app.schemas.campaign import CampaignCreate, CampaignOut, RecipientCreate
from app.services.tasks import enqueue_campaign_send


router = APIRouter(prefix="/campaigns", tags=["campaigns"])


@router.post("/", response_model=CampaignOut)
def create_campaign(payload: CampaignCreate, db: Session = Depends(get_db)):
    # Validate user and gmail account exist
    user = db.get(User, payload.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    account = db.get(GmailAccount, payload.sender_account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Gmail account not found")

    campaign = Campaign(
        user_id=payload.user_id,
        sender_account_id=payload.sender_account_id,
        name=payload.name,
        type=payload.type,
        status="draft",
        email_subject=payload.email_subject,
        html_content=payload.html_content,
        text_content=payload.text_content,
        settings_json=json.dumps(payload.settings or {}),
    )
    db.add(campaign)
    db.flush()

    # Optional recipients at creation
    for r in payload.recipients:
        recipient = Recipient(
            campaign_id=campaign.id,
            email=r.email,
            first_name=r.first_name,
            last_name=r.last_name,
            company=r.company,
            custom_fields_json=json.dumps(r.custom_fields or {}),
        )
        db.add(recipient)

    db.commit()
    db.refresh(campaign)
    return campaign


@router.post("/{campaign_id}/recipients")
def add_recipients(campaign_id: str, recipients: List[RecipientCreate], db: Session = Depends(get_db)):
    campaign = db.get(Campaign, campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    for r in recipients:
        recipient = Recipient(
            campaign_id=campaign.id,
            email=r.email,
            first_name=r.first_name,
            last_name=r.last_name,
            company=r.company,
            custom_fields_json=json.dumps(r.custom_fields or {}),
        )
        db.add(recipient)

    db.commit()
    return {"added": len(recipients)}


@router.post("/{campaign_id}/send")
def send_campaign(campaign_id: str, db: Session = Depends(get_db)):
    campaign = db.get(Campaign, campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    campaign.status = "active"
    db.add(campaign)
    db.commit()

    enqueue_campaign_send(str(campaign.id))
    return {"status": "queued"}


@router.get("/{campaign_id}", response_model=CampaignOut)
def get_campaign(campaign_id: str, db: Session = Depends(get_db)):
    campaign = db.get(Campaign, campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign