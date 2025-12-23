"""An AWS Python Pulumi program"""

import sys

sys.path.append("..")

from core import create_eks_cluster

create_eks_cluster("alex-test")
