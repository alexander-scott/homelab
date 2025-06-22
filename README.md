# Homelab

## Getting started

### Pre-requisites

First, ensure you have [UV](https://docs.astral.sh/uv/getting-started/installation/) installed on your local machine. Then, set up a virtual environment and install the dependencies from `requirements.txt` with:

```bash
uv venv
source .venv/bin/activate
uv sync
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

### The Homelab Machine

#### On-prem

If you want to run your homelab on-premises on a Raspberry Pi, ensure it is accessible on your local network and add your public key to its `~/.ssh/authorized_keys` file.

#### AWS

If you want to run the homelab on a disposable VM in the cloud, you need to create that. First, ensure your AWS account exists and you have full access. Next, make sure your local setup is correct, with the AWS config file pointing to your account and the correct role, and that your credentials are refreshed. You can check this with:

```bash
$ cat ~/.aws/credentials
[default]
aws_access_key_id = your-access-key-id
aws_secret_access_key = your-secret-access-key
aws_session_token = your-session-token
valid_until = 2025-06-23 01:30:58+00:00

$ cat ~/.aws/config
[profile 123456789_UserFull]
output=json
region=eu-central-1
role_arn=arn:aws:iam::123456789:role/fpc/UserFull
source_profile=default

$ export AWS_PROFILE=123456789_UserFull

$ aws sts get-caller-identity
{
    "UserId": "your-user-id",
    "Account": "your-account-id",
    "Arn": "your-arn"
}
```

Then, set your Pulumi cache to be within the current directory:

```bash
pulumi login file://.pulumi
```

Finally, copy the `aws/private_constants.py.example` file, rename it to `private_constants.py`, and provide your public key, AWS VPC, and subnet ID for the VM.

To check everything is working, run:

```bash
$ export AWS_PROFILE=123456789_UserFull
$ pulumi preview
Previewing update (homelab):
     Type                      Name             Plan
 +   pulumi:pulumi:Stack       project-homelab  create
 +   ├─ aws:ec2:KeyPair        test-keypair     create
 +   ├─ aws:ec2:SecurityGroup  test-sg          create
 +   ├─ aws:ec2:Instance       test-vm          create
 +   └─ aws:ec2:Eip            test-eip         create

Outputs:
    test-publicIp: [unknown]

Resources:
    + 5 to create
```
