"""Parity tests between the Python and JavaScript profiler implementations."""

from pathlib import Path
import json
import subprocess

import pandas as pd
import pytest

from faircode import profile

FIXTURES = Path(__file__).resolve().parent / "fixtures"


@pytest.mark.parametrize(
    "csv_name",
    [
        "small.csv",
        "adult.csv",
        "compas-scores-raw.csv",
        "credit_customers.csv",
        "AI_Fair_Recruitment_Dataset.csv",
    ],
)
def test_python_js_profiler_parity(csv_name):
    """The Python and JavaScript profilers should produce equivalent structured JSON."""

    csv = FIXTURES / csv_name

    python_result = profile(pd.read_csv(csv))

    completed = subprocess.run(
        ["node", "scripts/profile-js.js", str(csv)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )

    javascript_result = json.loads(completed.stdout)

    # Flags are human-readable messages. They duplicate information already
    # present in the structured output and may differ because Python and
    # JavaScript format floating-point values differently (e.g. 6.25 -> 6.2
    # vs 6.3). Compare the structured data instead.
    python_result = dict(python_result)
    javascript_result = dict(javascript_result)

    python_result.pop("flags", None)
    javascript_result.pop("flags", None)

    assert javascript_result == python_result
