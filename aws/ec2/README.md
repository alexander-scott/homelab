### The AWS Homelab Machine

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
mkdir .pulumi
pulumi login file://.pulumi
```

Finally, copy the `aws/private_constants.py.example` file, rename it to `private_constants.py`, and provide your public key, AWS VPC, and subnet ID for the VM.

To check everything is working, run:

```bash
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

You can then create the resources with:

```bash
$ pulumi up
```

And destroy them when you're done with:

```bash
$ pulumi destroy
```

Note: You'll need to pass `-C aws/ec2` if the current working directory is not the `aws/ec2` dir.

### Accessing the EC2 instance

On Linux, it can simply be accessed over SSH:

```bash
$ ssh -i ./ssh_keys/id_rsa ubuntu@{IP_ADDRESS}
```

On Windows, you can also access it over remote desktop. On Macos, the [`Windows app`](https://apps.apple.com/us/app/windows-app/id1295203466?mt=12) is a great way to do this and you just need to provide the IP address and username and password. The default username is `Administrator`, and the password will depend on the keys used. This can easily be retrieved via the AWS however:

```bash
$ aws ec2 describe-instances --filters "Name=instance-state-name,Values=running" --query 'Reservations[*].Instances[*].[InstanceId,InstanceType,State.Name,PublicIpAddress,PrivateIpAddress,Tags[?Key==`Name`].Value|[0]]' --output table
$ aws ec2 get-password-data --instance-id <instance-id> --priv-launch-key <path-to-pem-file>
```
