from phi.docker.app.jupyter import Jupyter
from phi.docker.resource.image import DockerImage

from workspace.settings import ws_settings

#
# -*- Run a Jupyter notebook on docker
#

# -*- Jupyter dev image
dev_jupyter_image = DockerImage(
    name=f"{ws_settings.image_repo}/jupyter-dp",
    tag=ws_settings.dev_env,
    enabled=ws_settings.build_images,
    path=str(ws_settings.ws_root),
    dockerfile="workspace/dev/jupyter/Dockerfile",
    pull=ws_settings.force_pull_images,
    # Uncomment to push the dev image
    # push_image=ws_settings.push_images,
    skip_docker_cache=ws_settings.skip_image_cache,
)

# Jupyter running on port 8888:8888
dev_jupyter_app = Jupyter(
    image=dev_jupyter_image,
    enabled=ws_settings.dev_airflow_enabled,
    mount_workspace=True,
    # Read secrets from secrets/dev_jupyter_secrets.yml
    secrets_file=ws_settings.ws_root.joinpath(
        "workspace/secrets/dev_jupyter_secrets.yml"
    ),
    use_cache=ws_settings.use_cache,
)
