from fastapi import FastAPI, Response, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from .utils import PIXEL_PNG

app = FastAPI(title="Outreach AI API")


@app.get("/")
async def read_root():
    """Health check endpoint."""
    return {"message": "Outreach AI API running"}


@app.get("/track/open/{message_id}.png")
async def track_open(message_id: str):
    """Return a transparent tracking pixel and record an open event."""
    # In a real implementation, record the open event in the database
    return Response(content=PIXEL_PNG, media_type="image/png")


@app.get("/track/click/{message_id}")
async def track_click(message_id: str, url: str):
    """Record a click event and redirect to the destination URL."""
    # In a real implementation, record the click event in the database
    return RedirectResponse(url)


@app.get("/unsubscribe/{recipient_id}")
async def unsubscribe(recipient_id: str):
    """Record an unsubscribe event and confirm to the user."""
    # In a real implementation, update the suppression list
    return {"message": "You have been unsubscribed."}


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    """Simple dashboard placeholder."""
    html = """
    <html>
    <head><title>Outreach Dashboard</title></head>
    <body>
    <h1>Campaign Dashboard</h1>
    <p>This is a placeholder for metrics and charts.</p>
    </body>
    </html>
    """
    return HTMLResponse(content=html, status_code=200)
