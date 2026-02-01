from enum import Enum

try:
    from private_constants import _PUBLIC_KEYPAIR, _SUBNET_ID, _SUBNET_ID_2, _VPC_ID

    VPC_ID = _VPC_ID
    SUBNET_ID = _SUBNET_ID
    SUBNET_ID_2 = _SUBNET_ID_2
    PUBLIC_KEYPAIR = _PUBLIC_KEYPAIR
except ImportError:
    VPC_ID = ""
    SUBNET_ID = ""
    SUBNET_ID_2 = ""
    PUBLIC_KEYPAIR = ""


class AMI_ID(str, Enum):  # noqa: N801
    UBUNTU_SERVER_2404 = "ami-0fd8fe5cdf7cad6f6"  # Ubuntu Server 24.04 LTS (HVM) (ARM)
    WINDOWS_SERVER_2025 = "ami-0fa2863f423f8795e"  # Windows_Server-2025-English-Full-EKS_Optimized-1.35-2026.01.22


# Finding AMI IDs
# - You can browse web here https://eu-central-1.console.aws.amazon.com/ec2/home?region=eu-central-1#Images:
# - Or do it programmatically:
# $ aws ec2 describe-images --owners 'amazon' --filters 'Name=platform,Values=windows' 'Name=name,Values=*Windows_Server-2025-*' --query 'reverse(sort_by(Images, &CreationDate))[*].{Architecture:Architecture, CreationDate:CreationDate, ImageId:ImageId, Name:Name}' --output table --region eu-central-1
