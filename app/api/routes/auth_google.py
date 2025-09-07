from typing import Optional
from urllib.parse import urlencode

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse, JSONResponse
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from itsdangerous import URLSafeSerializer, BadSignature
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.session import get_db, session_scope
from app.models.user import User
from app.models.gmail_account import GmailAccount
from app.security.crypto import encrypt_value


router = APIRouter(prefix="/auth/google", tags=["auth"])

SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.modify",
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
]
TOKEN_URI = "https://oauth2.googleapis.com/token"
AUTH_URI = "https://accounts.google.com/o/oauth2/auth"

settings = get_settings()
serializer = URLSafeSerializer(settings.secret_key, salt="oauth-state")


def _client_config():
    return {
        "web": {
            "client_id": settings.google_client_id,
            "client_secret": settings.google_client_secret,
            "redirect_uris": [settings.google_redirect_uri],
            "auth_uri": AUTH_URI,
            "token_uri": TOKEN_URI,
        }
    }


@router.get("/login")
def google_login(user_email: str, db: Session = Depends(get_db)):
    if not settings.google_client_id or not settings.google_client_secret:
        raise HTTPException(status_code=500, detail="Google OAuth not configured")

    user = db.scalar(select(User).where(User.email == user_email))
    if not user:
        user = User(email=user_email)
        db.add(user)
        db.commit()
        db.refresh(user)

    flow = Flow.from_client_config(
        _client_config(), scopes=SCOPES, redirect_uri=settings.google_redirect_uri
    )

    state = serializer.dumps({"user_id": str(user.id)})
    auth_url, _ = flow.authorization_url(
        access_type="offline", include_granted_scopes="true", prompt="consent", state=state
    )
    return RedirectResponse(url=auth_url)


@router.get("/callback")
def google_callback(request: Request, db: Session = Depends(get_db)):
    params = dict(request.query_params)
    error = params.get("error")
    if error:
        raise HTTPException(status_code=400, detail=f"OAuth error: {error}")

    state = params.get("state")
    if not state:
        raise HTTPException(status_code=400, detail="Missing state")

    try:
        payload = serializer.loads(state)
    except BadSignature:
        raise HTTPException(status_code=400, detail="Invalid state")

    user_id: str = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid state payload")

    flow = Flow.from_client_config(
        _client_config(), scopes=SCOPES, redirect_uri=settings.google_redirect_uri
    )
    authorization_response = str(request.url)
    flow.fetch_token(authorization_response=authorization_response)
    creds = flow.credentials

    # Fetch Gmail profile email
    service = build("gmail", "v1", credentials=creds, cache_discovery=False)
    profile = service.users().getProfile(userId="me").execute()
    email_address: Optional[str] = profile.get("emailAddress")
    if not email_address:
        raise HTTPException(status_code=400, detail="Unable to retrieve Gmail profile")

    account = GmailAccount(
        user_id=user_id,
        email_address=email_address,
        access_token_encrypted=encrypt_value(creds.token),
        refresh_token_encrypted=encrypt_value(creds.refresh_token) if creds.refresh_token else None,
        token_expiry=getattr(creds, "expiry", None),
        scopes=" ".join(creds.scopes or []),
    )
    db.add(account)
    db.commit()
    db.refresh(account)

    return JSONResponse({"status": "connected", "account_id": str(account.id), "email": email_address})