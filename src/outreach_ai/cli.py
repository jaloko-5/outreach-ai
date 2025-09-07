"""
CLI entry point for the outreach_ai package.

This module defines a simple command-line interface using Typer. It allows you to
initialize the database and start the API server. Additional commands can be
added later for sender management, recipient import, campaign creation, running
campaigns, and delivery loops.
"""

import typer
import uvicorn

from .db import engine
from .models import Base
from .app import app as fastapi_app

cli = typer.Typer(help="Command-line interface for Outreach AI")

@cli.command()
def db_init() -> None:
    """Initialize the database by creating all tables."""
    Base.metadata.create_all(bind=engine)
    typer.echo("Database initialized.")

@cli.command()
def server_start(
    host: str = typer.Option("127.0.0.1", help="Host to bind the FastAPI server."),
    port: int = typer.Option(8000, help="Port to bind the FastAPI server."),
    reload: bool = typer.Option(True, help="Enable auto-reload on code changes."),
) -> None:
    """Start the FastAPI server for tracking, click redirects, and dashboard."""
    uvicorn.run(fastapi_app, host=host, port=port, reload=reload)

@cli.command()
def deliver_loop() -> None:
    """
    Continuously deliver queued messages.

    This is a stub implementation. In a full implementation, this function would
    poll the database for messages ready to be sent, respect warm-up quotas,
    schedule windows, rotate senders, and use the senders module to send emails.
    """
    typer.echo("Delivery loop not yet implemented.")

def main() -> None:
    """Main entry point for the CLI."""
    cli()

if __name__ == "__main__":
    main()
