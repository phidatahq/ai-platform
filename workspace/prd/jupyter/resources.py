from phi.aws.resource.ec2 import EbsVolume
from phi.docker.resource.image import DockerImage
from phi.k8s.app.jupyter import Jupyter, AppVolumeType, ServiceType

from workspace.prd.aws.eks_cluster import workers_ng_label
from workspace.settings import ws_settings

# -*- Run jupyter notebooks on kubernetes

# -*- EbsVolume for jupyter lab
prd_jupyter_volume = EbsVolume(
    name=f"jupyter-{ws_settings.prd_key}",
    enabled=ws_settings.prd_jupyter_enabled,
    size=16,
    availability_zone=ws_settings.aws_az1,
    tags=ws_settings.prd_tags,
    skip_delete=False,
    save_output=True,
)

# -*- Jupyter lab image
prd_jupyter_image = DockerImage(
    name=f"{ws_settings.image_repo}/jupyter",
    tag=ws_settings.prd_env,
    enabled=ws_settings.build_images and ws_settings.prd_jupyter_enabled,
    path=str(ws_settings.ws_root),
    platform="linux/amd64",
    dockerfile="workspace/prd/jupyter/Dockerfile",
    pull=ws_settings.force_pull_images,
    push_image=ws_settings.push_images,
    skip_docker_cache=ws_settings.skip_image_cache,
)

# -*- Jupyter kubernetes resources
prd_jupyter_app = Jupyter(
    name="jupyter",
    image_name=prd_jupyter_image.name,
    image_tag=prd_jupyter_image.tag,
    enabled=ws_settings.prd_jupyter_enabled,
    volume_type=AppVolumeType.AwsEbs,
    ebs_volume=prd_jupyter_volume,
    secrets_file=ws_settings.ws_root.joinpath(
        "workspace/secrets/prd_jupyter_secrets.yml"
    ),
    pod_node_selector=workers_ng_label,
    # Expose the service using a load balancer
    service_type=ServiceType.LOAD_BALANCER,
    # To enable HTTPs, add an ACM certificate to the load balancer
    # Note: The domain should point to the loadbalancer in Route53
    # enable_https=True,
    # acm_certificate_arn="",
)
