from phi.docker.resource.image import DockerImage

from workspace.settings import ws_settings

# -*- Airflow production image
prd_airflow_image = DockerImage(
    name=f"{ws_settings.image_repo}/airflow-dp",
    tag=ws_settings.prd_env,
    enabled=ws_settings.build_images and ws_settings.prd_airflow_enabled,
    path=str(ws_settings.ws_root),
    platform="linux/amd64",
    dockerfile="workspace/prd/airflow/Dockerfile",
    pull=ws_settings.force_pull_images,
    push_image=ws_settings.push_images,
    skip_docker_cache=ws_settings.skip_image_cache,
)
