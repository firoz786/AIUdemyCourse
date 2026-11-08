"""
Day 15 - Production Engineering & Resilience: Centralized Logging Setup.

This file demonstrates the "observability" side of resilience: a production
agent should never fail silently, so we configure a single shared `logger`
that every other module imports and uses to record what's happening (attempts,
successes, retries, warnings, errors). Consistent, timestamped log messages
make it possible to diagnose failures after the fact instead of guessing.
"""

import logging

# Configure the root logging behavior once for the whole application: show
# INFO-level messages and above, formatted with a timestamp, severity level,
# and the message itself.
logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(message)s"
    )
)


# A single named logger shared across all modules in this project so logs
# are easy to filter/identify as coming from "agent".
logger = logging.getLogger(
    "agent"
)

