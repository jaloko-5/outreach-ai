"""Database models for Outreach AI using SQLAlchemy ORM."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base

# Base class for declarative models
Base = declarative_base()


class Sender(Base):
    __tablename__ = "senders"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    host = Column(String)
    port = Column(Integer)
    username = Column(String)
    password = Column(String)
    daily_limit = Column(Integer, default=0)


class Recipient(Base):
    __tablename__ = "recipients"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String, nullable=True)
    role = Column(String, nullable=True)
    company = Column(String, nullable=True)
    industry = Column(String, nullable=True)
    segment = Column(String, nullable=True)
    suppressed = Column(Boolean, default=False)


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    subject = Column(String)
    template_path = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    recipient_id = Column(Integer, ForeignKey("recipients.id"))
    sender_id = Column(Integer, ForeignKey("senders.id"))
    sent_at = Column(DateTime, nullable=True)
    opened_at = Column(DateTime, nullable=True)
    clicked_at = Column(DateTime, nullable=True)
    replied_at = Column(DateTime, nullable=True)
    status = Column(String, default="pending")


class Suppression(Base):
    __tablename__ = "suppression"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    reason = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
