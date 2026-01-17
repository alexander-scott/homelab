import pulumi
from constants import AMI_ID, PUBLIC_KEYPAIR, SUBNET_ID, VPC_ID
from pulumi_aws import ec2
from pulumi_command import local


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
        description="Enable HTTP/HTTPS and SSH access",
        vpc_id=vpc.id,
        ingress=[
            {  # Ping
                "protocol": "icmp",
                "from_port": 8,
                "to_port": 0,
                "cidr_blocks": ["0.0.0.0/0"],
            },
            {
                # SSH
                "protocol": "tcp",
                "from_port": 22,
                "to_port": 22,
                "cidr_blocks": ["0.0.0.0/0"],
            },
            {  # HTTP
                "protocol": "tcp",
                "from_port": 80,
                "to_port": 80,
                "cidr_blocks": ["0.0.0.0/0"],
            },
            {  # HTTPS
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
            {  # Necessary for K8s API https://kubernetes.io/docs/concepts/security/controlling-access/
                "protocol": "tcp",
                "from_port": 6443,
                "to_port": 6443,
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
        root_block_device={
            "volume_size": 100,
            "volume_type": "gp3",
            "delete_on_termination": True,
        },
    )

    lb = ec2.Eip(f"{resource_prefix}-eip", instance=instance.id, domain="vpc")

    pulumi.export(f"{resource_prefix}-publicIp", lb.public_ip)

    local.Command(
        "renderInventoryCmd",
        create="cat ../../ansible/inventory.yaml.example | envsubst > ../../ansible/private_inventory.yaml",
        environment={
            "ANSIBLE_HOST": lb.public_ip,
        },
    )
