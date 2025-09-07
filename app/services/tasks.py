import json
import math
from typing import List

from celery import shared_task
from sqlalchemy import select

from app.core.celery_app import celery
from app.db.session import session_scope
from app.models.campaign import Campaign
from app.models.recipient import Recipient
from app.services.gmail_service import send_email


BATCH_SIZE = 100  # Logical batch size
PACE_SECONDS = 2  # Basic pacing per email


def enqueue_campaign_send(campaign_id: str) -> None:
    # Kick off the first batch
    process_campaign_batch.apply_async(args=[campaign_id, 0])


@celery.task(name="process_campaign_batch")
def process_campaign_batch(campaign_id: str, offset: int = 0):
    with session_scope() as session:
        campaign = session.get(Campaign, campaign_id)
        if not campaign:
            return
        # Fetch a batch of recipients still pending
        recipients: List[Recipient] = (
            session.execute(
                select(Recipient)
                .where(Recipient.campaign_id == campaign_id)
                .where(Recipient.status == "pending")
                .offset(offset)
                .limit(BATCH_SIZE)
            )
            .scalars()
            .all()
        )

        if not recipients:
            campaign.status = "completed"
            session.add(campaign)
            return

        for index, r in enumerate(recipients):
            countdown = index * PACE_SECONDS
            send_single_email.apply_async(
                args=[campaign_id, str(r.id)], countdown=countdown
            )

        # Enqueue next batch
        next_offset = offset + len(recipients)
        process_campaign_batch.apply_async(args=[campaign_id, next_offset], countdown=max(1, len(recipients) * PACE_SECONDS // 2))


@celery.task(name="send_single_email")
def send_single_email(campaign_id: str, recipient_id: str):
    with session_scope() as session:
        campaign = session.get(Campaign, campaign_id)
        recipient = session.get(Recipient, recipient_id)
        if not campaign or not recipient:
            return

        subject = campaign.email_subject or ""
        html = campaign.html_content or ""
        text = campaign.text_content or ""
        try:
            send_email(
                account_id=str(campaign.sender_account_id),
                to_email=recipient.email,
                subject=subject,
                html=html,
                text=text,
            )
            recipient.status = "sent"
        except Exception:
            recipient.status = "failed"
        session.add(recipient)