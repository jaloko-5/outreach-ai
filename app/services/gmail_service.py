import base64
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

from app.security.crypto import decrypt_value, encrypt_value
from app.core.config import get_settings
from app.db.session import session_scope
from app.models.gmail_account import GmailAccount


TOKEN_URI = "https://oauth2.googleapis.com/token"
SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.modify",
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
]

settings = get_settings()


def _build_credentials(account: GmailAccount) -> Credentials:
    access_token = decrypt_value(account.access_token_encrypted)
    refresh_token = (
        decrypt_value(account.refresh_token_encrypted)
        if account.refresh_token_encrypted
        else None
    )

    creds = Credentials(
        token=access_token,
        refresh_token=refresh_token,
        token_uri=TOKEN_URI,
        client_id=settings.google_client_id,
        client_secret=settings.google_client_secret,
        scopes=SCOPES,
    )
    if account.token_expiry:
        creds.expiry = account.token_expiry
    return creds


def _persist_tokens(account: GmailAccount, creds: Credentials) -> None:
    account.access_token_encrypted = encrypt_value(creds.token)
    if creds.refresh_token:
        account.refresh_token_encrypted = encrypt_value(creds.refresh_token)
    account.token_expiry = getattr(creds, "expiry", None)
    account.scopes = " ".join(creds.scopes or [])


def get_gmail_service(account_id: str):
    with session_scope() as session:
        account: Optional[GmailAccount] = session.get(GmailAccount, account_id)
        if not account:
            raise ValueError("Gmail account not found")

        creds = _build_credentials(account)
        if not creds.valid and creds.refresh_token:
            creds.refresh(Request())
            _persist_tokens(account, creds)
            session.add(account)

        service = build("gmail", "v1", credentials=creds, cache_discovery=False)
        return service


def get_profile_email(account_id: str) -> str:
    service = get_gmail_service(account_id)
    profile = service.users().getProfile(userId="me").execute()
    return profile.get("emailAddress", "")


def send_email(account_id: str, to_email: str, subject: str, html: str, text: str = "") -> dict:
    service = get_gmail_service(account_id)

    msg = MIMEMultipart("alternative")
    msg["To"] = to_email
    msg["Subject"] = subject

    if text:
        msg.attach(MIMEText(text, "plain"))
    if html:
        msg.attach(MIMEText(html, "html"))

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode("utf-8")
    response = service.users().messages().send(userId="me", body={"raw": raw}).execute()
    return response