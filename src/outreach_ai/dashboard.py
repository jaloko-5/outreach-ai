"""Analytics and dashboard utilities.

This module defines helper functions to compute key performance metrics
for outreach campaigns. These metrics can then be displayed on a
simple dashboard to give users insight into how their emails are
performing over time.

The functions provided here are intentionally lightweight and do not
assume a specific database schema. They operate on numeric inputs and
return derived statistics.
"""

from __future__ import annotations

from typing import Iterable, List, Mapping, Dict


def success_percentage(total_sent: int, delivered: int) -> float:
    """Calculate the percentage of sent messages that were delivered.

    Args:
        total_sent: Total number of attempted sends.
        delivered: Number of messages that successfully reached the inbox.

    Returns:
        A float between 0 and 100 representing the success rate. If
        ``total_sent`` is zero, returns 0.0.
    """
    if total_sent <= 0:
        return 0.0
    return (delivered / total_sent) * 100.0


def engagement_rate(total_sent: int, opens: int, replies: int) -> Dict[str, float]:
    """Compute open and reply rates given counts.

    Args:
        total_sent: Total number of emails sent.
        opens: Number of messages opened.
        replies: Number of replies received.

    Returns:
        A dictionary with ``open_rate`` and ``reply_rate`` percentages.
    """
    if total_sent <= 0:
        return {"open_rate": 0.0, "reply_rate": 0.0}
    return {
        "open_rate": (opens / total_sent) * 100.0,
        "reply_rate": (replies / total_sent) * 100.0,
    }


def categorize_replies(replies: Iterable[str]) -> Dict[str, int]:
    """Naively categorize reply texts into simple categories.

    This is a placeholder demonstrating how replies might be categorized. In
    a real implementation, natural language processing or rules would be used.

    Args:
        replies: An iterable of reply texts.

    Returns:
        A mapping from category names to counts.
    """
    categories = {"positive": 0, "negative": 0, "other": 0}
    for reply in replies:
        text = reply.lower()
        if any(word in text for word in ("thank", "great", "interested")):
            categories["positive"] += 1
        elif any(word in text for word in ("no", "unsubscribe", "stop")):
            categories["negative"] += 1
        else:
            categories["other"] += 1
    return categories


def moving_average(data: List[float], window_size: int = 3) -> List[float]:
    """Compute a simple moving average over a list of numeric values.

    Args:
        data: List of numbers (e.g., daily engagement counts).
        window_size: Number of elements to include in each average.

    Returns:
        A list of averaged values. The result will be shorter than ``data``
        by ``window_size - 1`` elements.
    """
    if window_size <= 0:
        raise ValueError("window_size must be positive")
    if not data or len(data) < window_size:
        return []
    avgs: List[float] = []
    for i in range(len(data) - window_size + 1):
        window = data[i : i + window_size]
        avgs.append(sum(window) / window_size)
    return avgs


def render_dashboard(session):
    """
    Generate an HTML dashboard summary using the database session.

    Args:
        session: SQLAlchemy session.

    Returns:
        HTML string with metrics.
    """
    from .models import Event, Message

    total_messages = session.query(Message).count()
    open_count = session.query(Event).filter(Event.type == "open").count()
    click_count = session.query(Event).filter(Event.type == "click").count()
    unsub_count = session.query(Event).filter(Event.type == "unsub").count()

    # Compute percentages using helper functions
    success_pct = success_percentage(total_messages, open_count)
    open_rate = engagement_rate(total_messages, open_count)
    click_rate = engagement_rate(total_messages, click_count)
    unsub_rate = engagement_rate(total_messages, unsub_count)

    html = f"""
    <html>
      <head><title>Campaign Dashboard</title></head>
      <body>
        <h1>Campaign Dashboard</h1>
        <ul>
          <li>Success % (inbox placement): <b>{success_pct}</b></li>
          <li>Open rate: <b>{open_rate}</b></li>
          <li>Click rate: <b>{click_rate}</b></li>
          <li>Unsubscribes: <b>{unsub_count}</b></li>
        </ul>
      </body>
    </html>
    """
    return html
