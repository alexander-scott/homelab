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

### SSH

Ansible will be running tasks on the remote machine via ssh, therefore make sure you have created a key pair locally, and that your public key is present in the `~/.ssh/authorized_keys` file on the remote machine(s).

You can create a new key-pair with `ssh-keygen -t rsa -m PEM`.

### The homelab machine

#### On-prem

If you want to run your homelab on-prem on a Raspberry PI, then all you need to do is make sure it is accessible on your local network and add your public key to its `~/.ssh/authorized_keys` file.

#### AWS

If you want to run the homelab on a disposable VM in the cloud, we now need to create that. First, ensure your AWS account exists and you have full access there. Secondly, ensure that your local set up is correct with the AWS config file pointing to your account and the correct role, and that the credentials are refreshed. You can check this with:

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

Then, set your Pulumi cache to be within the current dir:

```bash
$ pulumi login file://.pulumi
```

Finally, copy the `aws/private_constants.py.example` file and rename it to `private_constants.py`, and then provide your public key and the AWS VPC and subnet ID that you want the VM to be created in.

To check everything is working you can run:

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
