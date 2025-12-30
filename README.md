# Homelab

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

## Single-node setups

### The On-prem Homelab Machine

If you want to run your homelab on-premises on a Raspberry Pi, ensure it is accessible on your local network and add your public key to its `~/.ssh/authorized_keys` file.

### The AWS Homelab Machine

See [`aws/ec2/README.md`](aws/ec2/README.md) for more details.

### Setup K3s on VM via Ansible

See [`ansible/README.md`](ansible/README.md) for more details.

## Multi-node setups

### AWS EKS

See [`aws/eks/README.md`](aws/eks/README.md) for more details.
