from phi.aws.resource.ec2 import EbsVolume
from phi.k8s.app.postgres import PostgresDb, AppVolumeType

from workspace.prd.aws.eks_cluster import services_ng_label
from workspace.settings import ws_settings

# -*- Run postgres databases on kubernetes

# -*- EbsVolume for postgres db
prd_postgres_volume = EbsVolume(
    name=f"postgres-{ws_settings.prd_key}",
    enabled=ws_settings.prd_db_enabled,
    size=32,
    availability_zone=ws_settings.aws_az1,
    tags=ws_settings.prd_tags,
    skip_delete=False,
    save_output=True,
)

# -*- Postgres App to use for production data
prd_postgres_app = PostgresDb(
    name="postgres",
    enabled=ws_settings.prd_db_enabled,
    volume_type=AppVolumeType.AwsEbs,
    ebs_volume=prd_postgres_volume,
    secrets_file=ws_settings.ws_root.joinpath(
        "workspace/secrets/prd_postgres_secrets.yml"
    ),
    pod_node_selector=services_ng_label,
)

# -*- Postgres connection ids for airflow
prd_postgres_connection_id = "postgres"
prd_postgres_airflow_connections = {
    prd_postgres_connection_id: prd_postgres_app.get_db_connection()
}
