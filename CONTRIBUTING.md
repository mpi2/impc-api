# Contributing

## Dependencies

The package is built with [uv](https://docs.astral.sh/uv/) and uses the `uv_build` backend declared in `pyproject.toml`.

## Installing the package for use

1. Clone the repository and navigate into it.
2. Run `uv sync` to create the project environment and install the package.
3. Try it out in Jupyter Notebook:


```
from impc_api import solr_request
num_found, df = solr_request( core='genotype-phenotype', params={
        'q': '*:*'
        'rows': 10
        'fl': 'marker_symbol,allele_symbol,parameter_stable_id'
    }
)
```

## Installing the package for development

We use [pytest](https://docs.pytest.org/en/stable/) for testing. The default `uv sync` includes the `dev` dependency group, which installs pytest.

```bash
uv run pytest
```

To run a specific test file:

```bash
uv run pytest tests/test_solr_request.py
```

## Building the package

To build the source distribution and wheel:

```bash
uv build
```

Local builds are only needed when checking packaging output; release builds are handled by the publish workflow.

## Making changes after installation

- Make changes to the `.py` modules as needed.
- If there are dependency changes, update `pyproject.toml`, run `uv lock` to update `uv.lock`, and run `uv sync` to install the updated dependencies in `.venv`.
- Re-run tests with `uv run pytest`.

- Your changes should have effect upon reloading the import of the package. For dependency changes, `uv sync` is sufficient to update the local environment.
