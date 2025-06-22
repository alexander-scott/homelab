"""An AWS Python Pulumi program"""

from common import spin_up_ec2_instance
from constants import AMI_ID

spin_up_ec2_instance("m8g.large", "test", AMI_ID.UBUNTU_SERVER_2404)
