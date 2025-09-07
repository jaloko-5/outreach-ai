"""Email sending utilities for outreach.

This module provides asynchronous helpers to send emails via SMTP using
``aiosmtplib``. It also supports a simulation mode controlled by the
``SIMULATION_MODE`` environment variable; when enabled, emails are not
actually sent but are instead logged for testing purposes.
"""

from __future__ import annotations

import logging
import os
from email.message import EmailMessage
from typing import Optional

import aiosmtplib  # type: ignore

# When SIMULATION_MODE is set to "1", messages will not be delivered.
SIMULATION_MODE: bool = os.getenv("SIMULATION_MODE", "1") == "1"


async def send_email(
    *,
    host: str,
    port: int,
    username: str,
    password: str,
    sender_email: str,
    recipient: str,
    subject: str,
    html_body: str,
    text_body: Optional[str] = None,
    start_tls: bool = True,
) -> None:
    """Send an email via SMTP or log it if in simulation mode.

    Args:
        host: SMTP server hostname.
        port: SMTP server port.
        username: SMTP username for authentication.
        password: SMTP password for authentication.
        sender_email: The email address of the sender.
        recipient: The recipient's email address.
        subject: Email subject line.
        html_body: HTML portion of the email body.
        text_body: Optional plain-text portion of the email body.
        start_tls: Whether to use STARTTLS for encryption.

    Raises:
        aiosmtplib.SMTPException: If sending fails when not in simulation mode.
    """
    # Build the email message
    message = EmailMessage()
    message["From"] = sender_email
    message["To"] = recipient
    message["Subject"] = subject
    if text_body:
        message.set_content(text_body)
    message.add_alternative(html_body, subtype="html")

    if SIMULATION_MODE:
        logging.info(
            "Simulating send to %s with subject %s", recipient, subject
        )
        return

    await aiosmtplib.send(
        message,
        hostname=host,
        port=port,
        username=username,
        password=password,
        start_tls=start_tls,
    )
