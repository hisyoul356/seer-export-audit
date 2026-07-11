# Contributing

Thank you for improving reproducible registry-research workflows.

## Before opening an issue or pull request

1. Never attach patient-level, restricted, or institution-owned data.
2. Use the synthetic fixtures in `examples/`, or provide a schema-only example.
3. State the expected and observed structural behaviour.
4. Run `python -m unittest discover -s tests -v` before submitting code.

## Pull requests

Keep pull requests small, document any new report field, and include a test for
behavioural changes. Features that parse a new dictionary format should include
only a synthetic fixture and a clear limitation statement.
