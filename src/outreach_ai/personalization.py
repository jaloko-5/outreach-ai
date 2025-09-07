"""Personalization utilities for Outreach AI emails."""
from typing import Dict
from jinja2 import Template


def render_template(template_str: str, context: Dict[str, str]) -> str:
    """Render a Jinja2 template string with the provided context.

    Args:
        template_str: The raw template string containing placeholders like {{ name }}.
        context: A dictionary of values to substitute into the template.

    Returns:
        A rendered string with the placeholders replaced by context values.
    """
    template = Template(template_str)
    return template.render(**context)
