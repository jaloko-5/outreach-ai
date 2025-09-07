"""Compliance utilities for outreach emails.

This module provides helpers to build CAN-SPAM and GDPR compliant email
components such as unsubscribe links, sender identification, and basic
suppression list checks. Using these functions helps ensure that all
outbound communication includes a clear way to opt out and proper
identification of the sender.
"""

from __future__ import annotations

from typing import Iterable, Set


def generate_unsubscribe_link(base_url: str, message_id: str) -> str:
    """Construct an unsubscribe URL for a given message.

    Args:
        base_url: The base URL of the tracking server (e.g. ``"https://example.com"``).
        message_id: Unique identifier for the message. This may be used to
            locate the recipient of the message on the backend.

    Returns:
        A fully-qualified URL that the recipient can visit to opt out.
    """
    base = base_url.rstrip("/")
    return f"{base}/unsubscribe?message_id={message_id}"


def generate_footer(sender_name: str, sender_email: str, unsubscribe_url: str) -> str:
    """Generate an HTML footer with sender info and unsubscribe link.

    Args:
        sender_name: Human-readable name of the sender.
        sender_email: Email address of the sender.
        unsubscribe_url: URL the recipient can click to unsubscribe.

    Returns:
        A string containing an HTML snippet to append to outgoing emails.
    """
    return (
        f"<p>--<br>{sender_name} &lt;{sender_email}&gt;<br>"
        f"<a href=\"{unsubscribe_url}\">Unsubscribe</a></p>"
    )


def is_suppressed(email: str, suppression_list: Iterable[str]) -> bool:
    """Determine whether a recipient's email is in the suppression list.

    The comparison is case-insensitive to ensure matches on normalized
    addresses.

    Args:
        email: The recipient's email address.
        suppression_list: An iterable of suppressed email addresses.

    Returns:
        ``True`` if ``email`` is suppressed, ``False`` otherwise.
    """
    normalized = email.strip().lower()
    return normalized in {e.strip().lower() for e in suppression_list}
