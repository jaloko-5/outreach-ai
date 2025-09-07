from sqlalchemy.orm import declarative_base


Base = declarative_base()

# Import models to register with SQLAlchemy metadata
# These imports are intentional side-effects
try:
    from app.models.user import User  # noqa: F401
    from app.models.gmail_account import GmailAccount  # noqa: F401
    from app.models.campaign import Campaign  # noqa: F401
    from app.models.recipient import Recipient  # noqa: F401
except Exception:
    # During certain tooling phases, models might not import cleanly; ignore.
    pass