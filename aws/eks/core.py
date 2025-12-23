import pulumi
import pulumi_eks as eks
import pulumi_kubernetes as k8s
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

    # Might need to do:
    # pulumi stack output kubeconfig > kubeconfig.yml
    # export KUBECONFIG=./kubeconfig.yml
    pulumi.export("kubeconfig", cluster.kubeconfig)

    test_ns = k8s.core.v1.Namespace(
        "test-namespace",
        pulumi.ResourceOptions(provider=cluster._provider),
    )

    # Use Helm to install the Nginx ingress controller
    k8s.helm.v3.Release(
        "ingresscontroller",
        chart="nginx-ingress",
        namespace=test_ns.metadata.name,
        repository_opts={
            "repo": "https://helm.nginx.com/stable",
        },
        skip_crds=True,
        values={
            "controller": {
                "enableCustomResources": False,
                "appprotect": {
                    "enable": False,
                },
                "appprotectdos": {
                    "enable": False,
                },
                "service": {
                    "extraLabels": {
                        "app": "nginx-ingress",
                    },
                },
            },
        },
        version="0.14.1",
    )

    deployment = k8s.apps.v1.Deployment(
        "whoami-deployment",
        metadata=k8s.meta.v1.ObjectMetaArgs(
            name="whoami-deployment",
            namespace=test_ns.metadata.name,
            labels={
                "app": "whoami",
            },
        ),
        spec=k8s.apps.v1.DeploymentSpecArgs(
            replicas=1,
            selector=k8s.meta.v1.LabelSelectorArgs(
                match_labels={
                    "app": "whoami",
                },
            ),
            template=k8s.core.v1.PodTemplateSpecArgs(
                metadata=k8s.meta.v1.ObjectMetaArgs(
                    labels={
                        "app": "whoami",
                    },
                ),
                spec=k8s.core.v1.PodSpecArgs(
                    containers=[
                        k8s.core.v1.ContainerArgs(
                            image="traefik/whoami",
                            name="whoami",
                            ports=[
                                k8s.core.v1.ContainerPortArgs(
                                    container_port=80,
                                )
                            ],
                        )
                    ],
                ),
            ),
        ),
    )

    whoami_svc = k8s.core.v1.Service(
        "whoami-svc",
        metadata=k8s.meta.v1.ObjectMetaArgs(
            name="whoami-svc",
            namespace=test_ns.metadata.name,
            labels={
                "app": "whoami",
            },
        ),
        spec=k8s.core.v1.ServiceSpecArgs(
            ports=[
                k8s.core.v1.ServicePortArgs(
                    port=80,
                    protocol="TCP",
                    target_port=80,
                )
            ],
            selector={
                "app": deployment.pulumi_resource_name,
            },
        ),
    )

    k8s.networking.v1.Ingress(
        "whoami-ingress",
        metadata=k8s.meta.v1.ObjectMetaArgs(
            name="whoami-ingress",
            namespace=test_ns.metadata.name,
            annotations={
                "nginx.ingress.kubernetes.io/rewrite-target": "/",
            },
        ),
        spec=k8s.networking.v1.IngressSpecArgs(
            ingress_class_name="nginx-ingress",
            rules=[
                k8s.networking.v1.IngressRuleArgs(
                    http=k8s.networking.v1.HTTPIngressRuleValueArgs(
                        paths=[
                            k8s.networking.v1.HTTPIngressPathArgs(
                                backend=k8s.networking.v1.IngressBackendArgs(
                                    service=k8s.networking.v1.IngressServiceBackendArgs(
                                        name=whoami_svc.pulumi_resource_name,
                                        port=k8s.networking.v1.ServiceBackendPortArgs(
                                            number=80,
                                        ),
                                    ),
                                ),
                                path="/",
                                path_type="Prefix",
                            )
                        ],
                    ),
                )
            ],
        ),
    )
