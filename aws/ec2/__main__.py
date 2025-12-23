"""An AWS Python Pulumi program"""

import sys

sys.path.append("..")

from constants import AMI_ID
from core import spin_up_ec2_instance

spin_up_ec2_instance("m8g.xlarge", "test", AMI_ID.UBUNTU_SERVER_2404)
