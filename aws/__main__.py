"""An AWS Python Pulumi program"""

from constants import AMI_ID
from ec2 import spin_up_ec2_instance

spin_up_ec2_instance("m8g.xlarge", "test", AMI_ID.UBUNTU_SERVER_2404)
