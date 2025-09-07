"""Scheduler utilities for email outreach.

This module provides functions to schedule email sends at random times within
specified windows to mimic human behavior and to allow for jitter in send times.
"""

from __future__ import annotations

import datetime
import random
from typing import Optional

try:
    # Python 3.9+
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover
    from backports.zoneinfo import ZoneInfo  # type: ignore


def next_send_time(
    *, start_hour: int = 9, end_hour: int = 17, timezone: str = "UTC"
) -> datetime.datetime:
    """Compute the next send time within a given daily window.

    The function randomly picks an hour, minute and second between
    ``start_hour`` and ``end_hour`` (exclusive) in the provided timezone.
    If the chosen time has already passed for today, it chooses a
    corresponding time on the following day.

    Args:
        start_hour: Earliest hour (0-23) to schedule sends.
        end_hour: Latest hour (1-24) to schedule sends; must be > ``start_hour``.
        timezone: IANA timezone string (e.g. "America/New_York").

    Returns:
        A timezone-aware ``datetime.datetime`` object representing the next
        scheduled send time in UTC.
    """
    if end_hour <= start_hour:
        raise ValueError("end_hour must be greater than start_hour")

    tz = ZoneInfo(timezone)
    now = datetime.datetime.now(tz)
    today = now.date()

    # Pick a random time within the window
    hour = random.randint(start_hour, end_hour - 1)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)

    candidate = datetime.datetime.combine(
        today, datetime.time(hour, minute, second), tzinfo=tz
    )

    # If the candidate time is in the past, schedule for tomorrow
    if candidate <= now:
        candidate += datetime.timedelta(days=1)

    return candidate.astimezone(datetime.timezone.utc)


def add_jitter(base_time: datetime.datetime, max_seconds: int = 300) -> datetime.datetime:
    """Add a random jitter to a base time.

    This can be used to vary send times slightly so that multiple emails
    scheduled for the same minute are spread out. The jitter is uniformly
    sampled between 0 and ``max_seconds``.

    Args:
        base_time: The original scheduled time (timezone-aware).
        max_seconds: Maximum number of seconds by which to delay the send.

    Returns:
        A new ``datetime.datetime`` adjusted by a positive random offset.
    """
    if max_seconds < 0:
        raise ValueError("max_seconds must be non-negative")
    offset = datetime.timedelta(seconds=random.randint(0, max_seconds))
    return base_time + offset
