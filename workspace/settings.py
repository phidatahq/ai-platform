from pathlib import Path

from phi.workspace.settings import WorkspaceSettings

#
# -*- Define workspace settings using a WorkspaceSettings object
# these values can also be set using environment variables.
#
ws_settings = WorkspaceSettings(
    # Workspace name: used for naming cloud resources
    ws_name="data-platform",
    # Path to the workspace root
    ws_root=Path(__file__).parent.parent.resolve(),
    # Workspace git repo url: used to git-sync DAGs and Charts
    ws_repo="https://github.com/phidatahq/data-platform.git",
    # -*- Dev settings
    dev_env="dev",
    # -*- Dev Apps
    dev_airflow_enabled=True,
    dev_jupyter_enabled=True,
    dev_db_enabled=True,
    # -*- Production settings
    prd_env="prd",
    # Production branch: used for git-sync
    # prd_branch: str = "main",
    # -*- Production Apps
    prd_airflow_enabled=True,
    prd_jupyter_enabled=True,
    prd_superset_enabled=True,
    prd_traefik_enabled=True,
    prd_whoami_enabled=True,
    prd_db_enabled=True,
    # -*- AWS settings
    # Region for AWS resources
    aws_region="us-east-2",
    # Availability Zones for AWS resources
    aws_az1="us-east-2a",
    aws_az2="us-east-2b",
    # Subnet IDs in the aws_region
    # EKS requires at least 2 subnets in different AZs.
    # More info: https://docs.aws.amazon.com/eks/latest/userguide/network_reqs.html
    # subnet_ids=["subnet-xyz", "subnet-xyz"],
    # -*- Image Settings
    # Repository for images (for example, to use ECR use the following format)
    # image_repo="[ACCOUNT_ID].dkr.ecr.us-east-2.amazonaws.com",
    # Build images locally
    # build_images=True,
    # Push images after building
    # push_images=True,
)
