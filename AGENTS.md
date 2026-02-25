# Agent Guide: IMPC API

This document provides context, rules, and guidelines for AI agents (like GitHub Copilot, Cursor, or Gemini) working on the `impc-api` codebase.

## 🛠 Tech Stack
- **Language**: Python 3.10+
- **Data Handling**: `pandas` (primary output format for dataframes)
- **Networking**: `requests` (for API calls)
- **Validation**: `pydantic` (for input/parameter validation)
- **Testing**: `pytest`
- **Progress Tracking**: `tqdm`
- **Environment**: Optimized for Jupyter Notebooks/Lab

## 📂 Project Structure
- `impc_api/`: Core package directory.
  - `solr_request.py`: Standard single-request logic.
  - `batch_solr_request.py`: Logic for large/chunked requests.
  - `utils/`:
    - `validators.py`: Pydantic models for core/field validation.
    - `core_fields.json`: Source of truth for valid Solr cores and their allowed fields.
    - `warnings.py`: Custom warning categories (e.g., `InvalidCoreWarning`).
- `tests/`: Unit and integration tests.

## 📏 Coding Conventions & Rules

### 1. Validation First
- Always validate `core` and `fl` (field list) parameters using `CoreParamsValidator` in `impc_api/utils/validators.py`.
- Validation should generally issue **Warnings** rather than raising Errors to avoid breaking user workflows, unless the request is physically impossible (e.g., unsupported download format).
- Refer to `impc_api/utils/core_fields.json` when suggesting new fields.

### 2. Jupyter Compatibility
- Maintain compatibility with `ipykernel` and `notebook`.
- Ensure output is clean and informative for notebook users (e.g., using `tqdm` for progress bars in batch requests).

### 3. Type Hinting
- Use explicit type hints for all function signatures and complex variables.
- Use `typing.Dict`, `typing.List`, and `typing.Optional` as needed.

### 4. Testing
- **Always** verify changes by running `pytest`.
- New features should include corresponding tests in `tests/`.
- Use `pytest.mark.parametrize` for testing multiple API scenarios.

## ⌨️ Key Commands
```bash
# Install for development
pip install -e .[dev]

# Run all tests
pytest

# Run a specific test file
pytest tests/test_solr_request.py

# Check linting (if configured)
# Currently, the project uses standard Python conventions.
```

## 🚧 Boundaries & Constraints
- **Secrets**: Never commit API keys or sensitive internal URLs. The IMPC API is public, but always double-check.
- **Dependencies**: Do not add new heavy dependencies without consulting the `pyproject.toml`.
- **API Strain**: When implementing new features, ensure they don't put unnecessary load on the IMPC Solr servers. Use `batch_size` defaults appropriately.

## 💡 Common Tasks
- **Updating Allowed Fields**: Add the field name to the corresponding core list in `impc_api/utils/core_fields.json`.
- **Modifying Validation**: Edit `impc_api/utils/validators.py` and ensure `pydantic` models are updated.
