# Homelab

## Getting started

### Pre-requisites

First, ensure you have [UV](https://docs.astral.sh/uv/getting-started/installation/) on your local machine, then set up a venv and install the deps in the `requirements.txt` with:

```bash
$ uv venv
$ source .venv/bin/activate
$ uv sync
```

You can also run the pre-commit linters with:

```bash
$ uv tool run -- pre-commit run --all-files
```
