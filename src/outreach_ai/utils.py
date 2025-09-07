"""Utility functions and constants for Outreach AI."""
import base64

# Base64 encoded 1x1 transparent PNG
PIXEL_PNG_BASE64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgYAAAAAMA"
    "AApW5gkAAAAASUVORK5CYII="
)

# Decode the tracking pixel once at import time
PIXEL_PNG: bytes = base64.b64decode(PIXEL_PNG_BASE64)


def get_tracking_pixel() -> bytes:
    """Return the binary contents of a 1x1 transparent PNG pixel."""
    return PIXEL_PNG
