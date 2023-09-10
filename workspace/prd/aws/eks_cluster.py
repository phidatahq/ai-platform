from phi.aws.resource.eks import EksCluster, EksKubeconfig, EksNodeGroup
from phi.resource.group import ResourceGroup

from workspace.settings import ws_settings

#
# -*- EKS Cluster for the Production Environment
#

# -*- Settings
# Label for running pods on the Services Node Group
services_ng_label = {"app_type": "service"}
# Label for running pods on the Workers Node Group
workers_ng_label = {"app_type": "worker"}
# Skip resource deletion when running `phi ws down`
skip_delete: bool = False
# Save resource outputs to workspace/outputs
save_output: bool = True

# -*- EKS cluster
prd_eks_cluster = EksCluster(
    name=f"{ws_settings.prd_key}-cluster",
    # To use your own subnets, uncomment the resources_vpc_config and add subnets
    # resources_vpc_config={
    #     "subnetIds": ws_settings.subnet_ids,
    # },
    # If resources_vpc_config is None, a default VPC Stack is created using
    # https://docs.aws.amazon.com/eks/latest/userguide/creating-a-vpc.html
    create_vpc_stack=True,
    tags=ws_settings.prd_tags,
    # Manage kubeconfig separately using the EksKubeconfig resource below
    manage_kubeconfig=False,
    skip_delete=skip_delete,
    save_output=save_output,
)

# -*- EKS Kubeconfig
prd_eks_kubeconfig = EksKubeconfig(eks_cluster=prd_eks_cluster)

# -*- EKS nodegroup for running core services
prd_services_nodegroup = EksNodeGroup(
    name=f"services-ng-{ws_settings.prd_key}",
    min_size=2,
    max_size=5,
    desired_size=2,
    disk_size=64,
    instance_types=["m5.large"],
    eks_cluster=prd_eks_cluster,
    # Add the services label to the nodegroup
    labels=services_ng_label,
    tags=ws_settings.prd_tags,
    skip_delete=skip_delete,
    save_output=save_output,
)

# -*- EKS nodegroup for running worker services
prd_worker_nodegroup = EksNodeGroup(
    name=f"workers-ng-{ws_settings.prd_key}",
    min_size=2,
    max_size=5,
    desired_size=2,
    disk_size=64,
    instance_types=["m5.large"],
    eks_cluster=prd_eks_cluster,
    # Add the workers label to the nodegroup
    labels=workers_ng_label,
    tags=ws_settings.prd_tags,
    skip_delete=skip_delete,
    save_output=save_output,
)

# -*- ResourceGroup for production EKS cluster
prd_eks_cluster_resources = ResourceGroup(
    name="eks",
    resources=[
        prd_eks_cluster,
        prd_eks_kubeconfig,
        prd_services_nodegroup,
        prd_worker_nodegroup,
    ],
)
