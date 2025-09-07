# Outreach AI

This repository contains a Python-based email outreach application inspired by Mystrika. It focuses on deliverability, personalization, analytics, compliance and scalability. Features include:

- **Deliverability & warm-up**: Gradually increase sending volume with randomized patterns to protect sender reputation and mimic human behavior.
- **Spam analysis & send pattern optimization**: Analyze content for spam triggers and optimize sending patterns (sender rotation, schedule randomization).
- **AI-powered personalization**: Use dynamic fields (recipient name, role, company, industry) to generate personalized email variants via Jinja2 templates or AI providers.
- **Engagement tracking & analytics**: Track delivery success, inbox placement, open rates, replies and pipeline attribution via a dashboard.
- **Compliance**: Automate unsubscribe links, sender identification and suppression list management (CAN-SPAM & GDPR).
- **Multi-account & scheduling**: Support multiple sender accounts and bulk scheduling to scale to thousands of recipients.

## Structure

The codebase is organized with a FastAPI server for tracking, SQLAlchemy models, CLI for campaign management, and utility modules for warm-up, scheduling, personalization, spam analysis and compliance.

See the [pyproject.toml](pyproject.toml) for dependencies and usage.
