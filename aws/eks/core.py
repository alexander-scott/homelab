import pulumi
import pulumi_eks as eks
from constants import SUBNET_ID, SUBNET_ID_2, VPC_ID
from pulumi_aws import ec2


def create_eks_cluster(project_name: str) -> None:
    vpc = ec2.get_vpc(id=VPC_ID)

    cluster = eks.Cluster(
        f"{project_name}",
        vpc_id=vpc.id,
        public_subnet_ids=[SUBNET_ID, SUBNET_ID_2],
        public_access_cidrs=["0.0.0.0/0"],
        desired_capacity=2,
        min_size=2,
        max_size=2,
        instance_type="t3.micro",
        # set storage class.
        storage_classes={
            "gp3": eks.StorageClassArgs(
                type="gp3",
                allow_volume_expansion=True,
                default=True,
                encrypted=True,
            )
        },
        enabled_cluster_log_types=[
            "api",
            "audit",
            "authenticator",
        ],
    )

    pulumi.export("kubeconfig", cluster.kubeconfig)
