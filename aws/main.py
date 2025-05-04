from .constants import AMI_ID
from .common import spin_up_ec2_instance


def spin_up_small_arm_ubuntu_2404() -> None:
    spin_up_ec2_instance("m8g.large", "test", AMI_ID.UBUNTU_SERVER_2404)
