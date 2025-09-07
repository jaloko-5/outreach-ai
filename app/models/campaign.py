import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    sender_account_id = Column(UUID(as_uuid=True), ForeignKey("gmail_accounts.id"), nullable=False)

    name = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False, default="cold_outreach")
    status = Column(String(50), nullable=False, default="draft")

    email_subject = Column(String(255), nullable=True)
    html_content = Column(Text, nullable=True)
    text_content = Column(Text, nullable=True)

    settings_json = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", backref="campaigns")
    sender_account = relationship("GmailAccount")