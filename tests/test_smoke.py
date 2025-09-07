"""Basic smoke tests to ensure modules import successfully."""


def test_imports():
    import importlib
    modules = [
        "outreach_ai.app",
        "outreach_ai.utils",
        "outreach_ai.db",
        "outreach_ai.models",
        "outreach_ai.personalization",
        "outreach_ai.analyzer",
        "outreach_ai.scheduler",
        "outreach_ai.warmup",
        "outreach_ai.compliance",
        "outreach_ai.senders",
        "outreach_ai.dashboard",
        "outreach_ai.cli",
    ]
    for mod in modules:
        importlib.import_module(mod)
