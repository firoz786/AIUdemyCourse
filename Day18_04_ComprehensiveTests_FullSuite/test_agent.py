"""
Day 18.04 - Comprehensive Tests (Full Suite) - full pipeline smoke test.

This is the biggest manual demo script in the course: it runs the full
research_agent loop (plan -> search -> read -> note -> verify) to
completion, then pulls the verified notes and feeds them into
generate_report() to produce a final written report. It exercises
almost every function in agent.py and tools.py in one end-to-end pass.
"""

# Import the two top-level agent entry points we're exercising.
from agent import (
    research_agent,
    generate_report
)

# Import the helper that filters research notes down to verified ones.
from tools import (
    get_verified_research_notes
)


# A sample research request to drive the agent with.
request = (
    "Research the role of AI agents "
    "in software development. "
    "Identify major use cases, benefits, "
    "and limitations."
)


# Run the full agent loop (allowing up to 100 steps) - this performs the
# searching, reading, note-taking, and verification internally.
research_agent(
    request,
    max_steps=100
)


# Pull out only the findings the agent actually verified.
verified_notes = (
    get_verified_research_notes()
)


if not verified_notes:

    # If nothing was verified, there's nothing meaningful to report on,
    # so stop here instead of generating an empty/fabricated report.
    print(
        "\nNo verified research findings "
        "were collected."
    )

    raise SystemExit



print(
    "\nVerified findings:",
    len(verified_notes)
)


# Turn the verified findings into a structured, human-readable report.
report = generate_report(
    user_request=request,
    verified_notes=verified_notes
)


print("\n")
print("=" * 60)
print("FINAL RESEARCH REPORT")
print("=" * 60)
print("\n")

print(report)
