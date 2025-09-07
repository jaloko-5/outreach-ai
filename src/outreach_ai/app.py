from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from .utils import PIXEL_PNG
from .db import SessionLocal, init_db
from .models import Event, Recipient
from .dashboard import render_dashboard


app = FastAPI(title="Outreach AI API")

@app.on_event("startup")
def _startup():
    """Initialize the database on startup."""
    init_db()


@app.get("/")
async def read_root():
    """Health check endpoint."""
    return {"message": "Outreach AI API running"}


@app.get("/track/open/{message_id}.png")
async def track_open(message_id: str):
    """Return a transparent tracking pixel and record an open event."""
    with SessionLocal() as session:
        session.add(Event(message_id=message_id, type="open", meta=None))
        session.commit()
    return Response(content=PIXEL_PNG, media_type="image/png")


@app.get("/track/click/{message_id}")
async def track_click(message_id: str, url: str):
    """Record a click event and redirect to the destination URL."""
    with SessionLocal() as session:
        session.add(Event(message_id=message_id, type="click", meta={"url": url}))
        session.commit()
    return RedirectResponse(url)


@app.get("/unsubscribe/{recipient_id}")
async def unsubscribe(recipient_id: int):
    """Record an unsubscribe event and confirm to the user."""
    with SessionLocal() as session:
        recipient = session.get(Recipient, recipient_id)
        if recipient:
            recipient.suppressed = True
        # Record the unsubscribe event
        session.add(Event(message_id=f"recipient-{recipient_id}", type="unsub", meta=None))
        session.commit()
    return {"message": "You have been unsubscribed."}


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    """Render the campaign dashboard with metrics."""
    with SessionLocal() as session:
        html = render_dashboard(session)
    return HTMLResponse(content=html, status_code=200)
