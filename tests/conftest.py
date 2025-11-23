import os

# Disable ANSI color codes during tests for stable output matching.
os.environ.setdefault("NO_COLOR", "1")
os.environ.setdefault("RICH_COLOR_SYSTEM", "none")
