## Getting started

### Pre-requisites

First, ensure you have [UV](https://docs.astral.sh/uv/getting-started/installation/) installed on your local machine. Then, set up a virtual environment and install the dependencies from `pyproject.toml` file with:

```bash
uv sync
source .venv/bin/activate
```

You can also run the pre-commit linters with:

```bash
uv tool run -- pre-commit run --all-files
```

### SSH

Ansible will run tasks on the remote machine via SSH. Make sure you have created a key pair locally, and that your public key is present in the `~/.ssh/authorized_keys` file on the remote machine(s).

You can create a new key pair with:

```bash
ssh-keygen -t rsa -m PEM
```
