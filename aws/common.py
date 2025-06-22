import pulumi
from pulumi_aws import ec2

from .constants import VPC_ID, SUBNET_ID, PUBLIC_KEYPAIR, AMI_ID


def spin_up_ec2_instance(
    instance_type: str, resource_prefix: str, ami_id: AMI_ID
) -> None:
    ami = ec2.get_ami(
        most_recent=True,
        owners=["amazon"],
        filters=[
            {
                "name": "image-id",
                "values": [ami_id],
            }
        ],
    )

    vpc = ec2.get_vpc(id=VPC_ID)
    subnet_1a = ec2.get_subnet(id=SUBNET_ID)

    group = ec2.SecurityGroup(
        f"{resource_prefix}-sg",
        description="Enable HTTP and SSH access",
        vpc_id=vpc.id,
        ingress=[
            {
                "protocol": "icmp",
                "from_port": 8,
                "to_port": 0,
                "cidr_blocks": ["0.0.0.0/0"],
            },
            {
                "protocol": "tcp",
                "from_port": 22,
                "to_port": 22,
                "cidr_blocks": ["0.0.0.0/0"],
            },
            {
                "protocol": "tcp",
                "from_port": 80,
                "to_port": 80,
                "cidr_blocks": ["0.0.0.0/0"],
            },
            {
                "protocol": "tcp",
                "from_port": 443,
                "to_port": 443,
                "cidr_blocks": ["0.0.0.0/0"],
            },
            {  # Necessary for Windows RDP https://en.wikipedia.org/wiki/Remote_Desktop_Protocol
                "protocol": "tcp",
                "from_port": 3389,
                "to_port": 3389,
                "cidr_blocks": ["0.0.0.0/0"],
            },
        ],
        # Unlimited outbound internet traffic
        egress=[
            {
                "protocol": "-1",
                "from_port": 0,
                "to_port": 0,
                "cidr_blocks": ["0.0.0.0/0"],
            },
        ],
    )

    key_pair = ec2.KeyPair(
        f"{resource_prefix}-keypair",
        key_name=f"{resource_prefix}-keypair",
        public_key=PUBLIC_KEYPAIR,
    )

    instance = ec2.Instance(
        f"{resource_prefix}-vm",
        instance_type=instance_type,
        ami=ami.id,
        subnet_id=subnet_1a.id,
        vpc_security_group_ids=[group.id],
        key_name=key_pair.key_name,
    )

    lb = ec2.Eip(f"{resource_prefix}-eip", instance=instance.id, domain="vpc")

    pulumi.export(f"{resource_prefix}-publicIp", lb.public_ip)
