"""Warm-up utilities for email outreach.

This module contains simple functions to compute sending quotas during domain
warm-up. The goal of a warm-up phase is to gradually increase the number
of emails sent per day to build sender reputation and avoid deliverability
issues. The functions below implement a geometric growth schedule and allow
customization of the base volume, growth multiplier and maximum quota.
"""

from __future__ import annotations

from typing import List


def daily_quota(
    day: int,
    base: int = 10,
    multiplier: float = 1.5,
    max_quota: int = 1000,
) -> int:
    """Compute the allowed number of messages for a given warm-up day.

    The quota grows geometrically by ``multiplier`` each day starting
    from ``base`` and is capped at ``max_quota``.

    Args:
        day: Zero-based day index (0 for the first day of warm-up).
        base: Initial number of messages on day 0.
        multiplier: Daily growth factor (e.g. 1.2 for 20% growth).
        max_quota: Maximum number of messages per day.

    Returns:
        The number of messages that may be sent on the given day.
    """
    if day < 0:
        raise ValueError("day must be non-negative")
    quota = int(base * (multiplier ** day))
    return min(quota, max_quota)


def generate_quota_schedule(
    days: int,
    base: int = 10,
    multiplier: float = 1.5,
    max_quota: int = 1000,
) -> List[int]:
    """Generate a warm-up quota schedule for a number of days.

    Args:
        days: Total number of warm-up days.
        base: Initial number of messages on day 0.
        multiplier: Daily growth factor.
        max_quota: Maximum number of messages per day.

    Returns:
        A list of quotas, one per day.
    """
    if days < 1:
        raise ValueError("days must be at least 1")
    return [daily_quota(day, base, multiplier, max_quota) for day in range(days)]
