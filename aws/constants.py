from enum import Enum

try:
    from private_constants import _VPC_ID, _SUBNET_ID, _PUBLIC_KEYPAIR

    VPC_ID = _VPC_ID
    SUBNET_ID = _SUBNET_ID
    PUBLIC_KEYPAIR = _PUBLIC_KEYPAIR
except ImportError:
    VPC_ID = ""
    SUBNET_ID = ""
    PUBLIC_KEYPAIR = ""


class AMI_ID(str, Enum):
    UBUNTU_SERVER_2404 = "ami-0fd8fe5cdf7cad6f6"  # Ubuntu Server 24.04 LTS (HVM) (ARM)
    WINDOWS_SERVER_2025 = (
        "ami-02875f678fa0d1eb2"  # Microsoft Windows Server 2025 Full Locale English
    )


# Finding AMI IDs
# - You can browse web here https://eu-central-1.console.aws.amazon.com/ec2/home?region=eu-central-1#Images:
# - Or do it programmatically:
# $ aws ec2 describe-images --owners 'amazon' --filters 'Name=platform,Values=windows' 'Name=name,Values=*Windows_Server-2025-*' --query 'reverse(sort_by(Images, &CreationDate))[*].{Architecture:Architecture, CreationDate:CreationDate, ImageId:ImageId, Name:Name}' --output table --region eu-central-1
