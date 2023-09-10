from pathlib import Path
from typing import Dict

from phi.app.group import AppGroup
from phi.docker.app.airflow import AirflowScheduler, AirflowWebserver, AirflowWorker
from phi.docker.app.postgres import PostgresDb
from phi.docker.app.redis import Redis
from phi.docker.resource.image import DockerImage

from workspace.dev.postgres import dev_postgres_airflow_connections
from workspace.settings import ws_settings

#
# -*- Airflow Docker resources
#

# -*- Airflow db: A postgres instance running on port 8320:5432
dev_airflow_db = PostgresDb(
    name="airflow-db",
    db_user="airflow",
    db_password="airflow",
    db_schema="airflow",
    # Connect to airflow db on port 8320
    host_port=8320,
)

# -*- Airflow redis: A redis instance running on port 8321:6379
dev_airflow_redis = Redis(
    name="airflow-redis",
    command=["redis-server", "--save", "60", "1"],
    host_port=8321,
)

# -*- Settings
# waits for airflow-db to be ready before starting app
wait_for_db: bool = True
# waits for airflow-redis to be ready before starting app
wait_for_redis: bool = True
# Airflow executor to use
executor: str = "CeleryExecutor"
# Mount the ws_repo using a docker volume
mount_workspace: bool = True
# Read secrets from secrets/dev_airflow_secrets.yml
secrets_file: Path = ws_settings.ws_root.joinpath(
    "workspace/secrets/dev_airflow_secrets.yml"
)
# Environment variables for airflow containers
airflow_env: Dict[str, str] = {
    "AIRFLOW_ENV": "dev",
    "AIRFLOW__WEBSERVER__EXPOSE_CONFIG": "True",
    "AIRFLOW__WEBSERVER__EXPOSE_HOSTNAME": "True",
    "AIRFLOW__WEBSERVER__EXPOSE_STACKTRACE": "True",
    # Create aws_default connection_id
    "AWS_DEFAULT_REGION": ws_settings.aws_region,
    "AIRFLOW_CONN_AWS_DEFAULT": "aws://",
}

# -*- Airflow dev image
dev_airflow_image = DockerImage(
    name=f"{ws_settings.image_repo}/airflow-dp",
    tag=ws_settings.dev_env,
    enabled=ws_settings.build_images,
    path=str(ws_settings.ws_root),
    # platform="linux/amd64",
    dockerfile="workspace/dev/airflow/Dockerfile",
    pull=ws_settings.force_pull_images,
    # Uncomment to push the dev image
    # push_image=ws_settings.push_images,
    skip_docker_cache=ws_settings.skip_image_cache,
)

# -*- Airflow webserver running on port 8080:8080
dev_airflow_webserver = AirflowWebserver(
    image=dev_airflow_image,
    db_app=dev_airflow_db,
    wait_for_db=wait_for_db,
    redis_app=dev_airflow_redis,
    wait_for_redis=wait_for_db,
    executor=executor,
    mount_workspace=mount_workspace,
    env_vars=airflow_env,
    secrets_file=secrets_file,
    use_cache=ws_settings.use_cache,
    db_connections=dev_postgres_airflow_connections,
    # Wait for scheduler to initialize airflow db -- mark as false after first run
    wait_for_db_init=True,
    # Set debug_mode to true to keep container if it crashes
    debug_mode=True,
)

# -*- Airflow scheduler
dev_airflow_scheduler = AirflowScheduler(
    image=dev_airflow_image,
    db_app=dev_airflow_db,
    wait_for_db=wait_for_db,
    redis_app=dev_airflow_redis,
    wait_for_redis=wait_for_redis,
    executor=executor,
    mount_workspace=mount_workspace,
    env_vars=airflow_env,
    secrets_file=secrets_file,
    use_cache=ws_settings.use_cache,
    db_connections=dev_postgres_airflow_connections,
    # Migrate (init/uprade) airflow db on container start
    db_migrate=True,
    # Creates airflow user: admin, pass: admin -- mark as false after first run
    create_airflow_admin_user=True,
    debug_mode=True,
)

# -*- Airflow worker serving the default & tier_1 workflows
dev_airflow_worker = AirflowWorker(
    queue_name="default,tier_1",
    image=dev_airflow_image,
    db_app=dev_airflow_db,
    wait_for_db=wait_for_db,
    redis_app=dev_airflow_redis,
    wait_for_redis=wait_for_redis,
    executor=executor,
    mount_workspace=mount_workspace,
    env_vars=airflow_env,
    secrets_file=secrets_file,
    use_cache=ws_settings.use_cache,
    db_connections=dev_postgres_airflow_connections,
    # Wait for scheduler to initialize airflow db -- mark as false after first run
    wait_for_db_init=True,
    debug_mode=True,
)

# -*- AppGroup for the airflow docker apps
dev_airflow_apps = AppGroup(
    name="airflow",
    enabled=ws_settings.dev_airflow_enabled,
    apps=[
        dev_airflow_db,
        dev_airflow_redis,
        dev_airflow_scheduler,
        dev_airflow_webserver,
        dev_airflow_worker,
    ],
)
