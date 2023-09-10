from pathlib import Path
from typing import Dict

from phi.app.group import AppGroup
from phi.k8s.app.superset import (
    SupersetInit,
    SupersetWebserver,
    SupersetWorker,
    SupersetWorkerBeat,
    ImagePullPolicy,
    ServiceType,
)
from phi.k8s.app.postgres import PostgresDb, AppVolumeType
from phi.k8s.app.redis import Redis

from workspace.prd.aws.eks_cluster import services_ng_label, workers_ng_label
from workspace.prd.superset.aws_resources import (
    use_rds,
    use_elasticache,
    prd_superset_db_volume,
    prd_superset_redis_volume,
)
from workspace.prd.superset.docker_resources import prd_superset_image
from workspace.settings import ws_settings

#
# -*- Superset Kubernetes resources
#

# -*- Superset db: A postgres instance to use as the database for superset
prd_superset_db = PostgresDb(
    name="ss-db",
    enabled=(not use_rds),
    volume_type=AppVolumeType.AwsEbs,
    ebs_volume=prd_superset_db_volume,
    secrets_file=ws_settings.ws_root.joinpath(
        "workspace/secrets/prd_superset_db_secrets.yml"
    ),
    pod_node_selector=services_ng_label,
)

# -*- Superset redis: A redis instance to use as the celery backend for superset
prd_superset_redis = Redis(
    name="ss-redis",
    enabled=(not use_elasticache),
    volume_type=AppVolumeType.AwsEbs,
    ebs_volume=prd_superset_redis_volume,
    command=["redis-server", "--save", "60", "1"],
    pod_node_selector=services_ng_label,
)

# -*- Settings
# waits for superset-db to be ready before starting app
wait_for_db: bool = True
# waits for superset-redis to be ready before starting app
wait_for_redis: bool = True
# Mount the workspace repo using git-sync
mount_workspace: bool = False
# Enabe git-sync to load the workspace repo from git
enable_gitsync: bool = True
# Read secrets from secrets/prd_superset_secrets.yml
prd_superset_secrets_file: Path = ws_settings.ws_root.joinpath(
    "workspace/secrets/prd_superset_secrets.yml"
)

# -*- Database configuration
# Add database configuration to the secrets when using RDS
db_user = prd_superset_db.get_db_user() if not use_rds else None
db_password = prd_superset_db.get_db_password() if not use_rds else None
db_schema = prd_superset_db.get_db_schema() if not use_rds else None
db_dialect = "postgresql"
db_host = prd_superset_db.get_db_host() if not use_rds else None
db_port = prd_superset_db.get_db_port() if not use_rds else None

# -*- Redis configuration
# Add redis configuration to the secrets when using Elasticache
redis_driver = "rediss" if use_elasticache else "redis"
redis_host = prd_superset_redis.get_db_host() if not use_elasticache else None
redis_port = prd_superset_redis.get_db_port() if not use_elasticache else None

# -*- Superset webserver
prd_superset_ws = SupersetWebserver(
    replicas=2,
    image_name=prd_superset_image.name,
    image_tag=prd_superset_image.tag,
    wait_for_db=wait_for_db,
    db_user=db_user,
    db_password=db_password,
    db_schema=db_schema,
    db_dialect=db_dialect,
    db_host=db_host,
    db_port=db_port,
    wait_for_redis=wait_for_redis,
    redis_driver=redis_driver,
    redis_host=redis_host,
    redis_port=redis_port,
    mount_workspace=mount_workspace,
    enable_gitsync=enable_gitsync,
    gitsync_repo=ws_settings.ws_repo,
    gitsync_ref=ws_settings.prd_branch,
    secrets_file=prd_superset_secrets_file,
    image_pull_policy=ImagePullPolicy.ALWAYS,
    use_cache=ws_settings.use_cache,
    pod_node_selector=services_ng_label,
    # Expose the service using a load balancer
    service_type=ServiceType.LOAD_BALANCER,
    # To enable HTTPs, add an ACM certificate to the load balancer
    # Note: The domain should point to the loadbalancer in Route53
    # enable_https=True,
    # acm_certificate_arn="",
)

# -*- Superset init
superset_init_enabled = True  # Mark as False after first run
prd_superset_init = SupersetInit(
    enabled=superset_init_enabled,
    image_name=prd_superset_image.name,
    image_tag=prd_superset_image.tag,
    wait_for_db=wait_for_db,
    db_user=db_user,
    db_password=db_password,
    db_schema=db_schema,
    db_dialect=db_dialect,
    db_host=db_host,
    db_port=db_port,
    wait_for_redis=wait_for_redis,
    redis_driver=redis_driver,
    redis_host=redis_host,
    redis_port=redis_port,
    mount_workspace=mount_workspace,
    enable_gitsync=enable_gitsync,
    gitsync_repo=ws_settings.ws_repo,
    gitsync_ref=ws_settings.prd_branch,
    secrets_file=prd_superset_secrets_file,
    image_pull_policy=ImagePullPolicy.ALWAYS,
    use_cache=ws_settings.use_cache,
    pod_node_selector=workers_ng_label,
)

# -*- Superset worker
prd_superset_worker = SupersetWorker(
    replicas=1,
    image_name=prd_superset_image.name,
    image_tag=prd_superset_image.tag,
    wait_for_db=wait_for_db,
    db_user=db_user,
    db_password=db_password,
    db_schema=db_schema,
    db_dialect=db_dialect,
    db_host=db_host,
    db_port=db_port,
    wait_for_redis=wait_for_redis,
    redis_driver=redis_driver,
    redis_host=redis_host,
    redis_port=redis_port,
    mount_workspace=mount_workspace,
    enable_gitsync=enable_gitsync,
    gitsync_repo=ws_settings.ws_repo,
    gitsync_ref=ws_settings.prd_branch,
    secrets_file=prd_superset_secrets_file,
    image_pull_policy=ImagePullPolicy.ALWAYS,
    use_cache=ws_settings.use_cache,
    pod_node_selector=workers_ng_label,
)

# -*- Superset worker beat
prd_superset_worker_beat = SupersetWorkerBeat(
    replicas=1,
    image_name=prd_superset_image.name,
    image_tag=prd_superset_image.tag,
    wait_for_db=wait_for_db,
    db_user=db_user,
    db_password=db_password,
    db_schema=db_schema,
    db_dialect=db_dialect,
    db_host=db_host,
    db_port=db_port,
    wait_for_redis=wait_for_redis,
    redis_driver=redis_driver,
    redis_host=redis_host,
    redis_port=redis_port,
    mount_workspace=mount_workspace,
    enable_gitsync=enable_gitsync,
    gitsync_repo=ws_settings.ws_repo,
    gitsync_ref=ws_settings.prd_branch,
    secrets_file=prd_superset_secrets_file,
    image_pull_policy=ImagePullPolicy.ALWAYS,
    use_cache=ws_settings.use_cache,
    pod_node_selector=workers_ng_label,
)

# -*- AppGroup for the superset kubernetes apps
prd_superset_apps = AppGroup(
    name="superset",
    enabled=ws_settings.prd_superset_enabled,
    apps=[
        prd_superset_db,
        prd_superset_redis,
        prd_superset_ws,
        prd_superset_init,
        prd_superset_worker,
        prd_superset_worker_beat,
    ],
)
