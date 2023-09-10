from phi.aws.resource.ec2 import EbsVolume
from phi.aws.resource.elasticache import CacheCluster, CacheSubnetGroup
from phi.aws.resource.rds import DbInstance, DbSubnetGroup
from phi.aws.resource.reference import AwsReference
from phi.aws.resource.secret import SecretsManager
from phi.resource.group import ResourceGroup

from workspace.prd.aws.eks_cluster import prd_eks_cluster
from workspace.settings import ws_settings

#
# -*- Airflow AWS resources
#   - If use_rds is True, create a RDS database instance,
#       otherwise run postgres on k8s using an EBS volume
#   - If use_elasticache is True, create a ElastiCache redis cluster,
#       otherwise run redis on k8s using an EBS volume

# -*- Settings
# If True, use RDS as database, otherwise run postgres on k8s
use_rds: bool = False
# If True, use ElastiCache as cache, otherwise run redis on k8s
use_elasticache: bool = False
# Skip resource deletion when running `phi ws down`
skip_delete: bool = False
# Save resource outputs to workspace/outputs
save_output: bool = True

# -*- EbsVolumes for airflow database and cache on k8s
# NOTE: For production, use RDS and ElastiCache instead of running postgres/redis on k8s.
# -*- EbsVolume for airflow-db
prd_airflow_db_volume = EbsVolume(
    name=f"airflow-db-{ws_settings.prd_key}",
    enabled=(not use_rds),
    size=32,
    tags=ws_settings.prd_tags,
    availability_zone=ws_settings.aws_az1,
    skip_delete=skip_delete,
    save_output=save_output,
)
# -*- EbsVolume for airflow-redis
prd_airflow_redis_volume = EbsVolume(
    name=f"airflow-redis-{ws_settings.prd_key}",
    enabled=(not use_elasticache),
    size=16,
    tags=ws_settings.prd_tags,
    availability_zone=ws_settings.aws_az1,
    skip_delete=skip_delete,
    save_output=save_output,
)

# -*- Subnet Group for airflow RDS Database
prd_airflow_db_subnet_group = DbSubnetGroup(
    name=f"airflow-db-sg-{ws_settings.prd_key}",
    enabled=use_rds,
    subnet_ids=AwsReference(prd_eks_cluster.get_subnets_in_order),
    skip_delete=skip_delete,
    save_output=save_output,
)

# -*- Subnet Group for airflow ElastiCache Cluster
prd_airflow_redis_subnet_group = CacheSubnetGroup(
    name=f"airflow-redis-sg-{ws_settings.prd_key}",
    enabled=use_elasticache,
    subnet_ids=AwsReference(prd_eks_cluster.get_subnets_in_order),
    skip_delete=skip_delete,
    save_output=save_output,
)

# -*- Secrets for airflow RDS Database
prd_airflow_db_secret = SecretsManager(
    name=f"airflow-db-secret-{ws_settings.prd_key}",
    enabled=use_rds,
    secret_files=[
        ws_settings.ws_root.joinpath("workspace/secrets/prd_airflow_db_secrets.yml")
    ],
    skip_delete=skip_delete,
    save_output=save_output,
)

# -*- Airflow RDS Database Instance
db_engine = "postgres"
prd_airflow_rds_db = DbInstance(
    name=f"airflow-db-{ws_settings.prd_key}",
    enabled=use_rds,
    engine=db_engine,
    engine_version="15.3",
    allocated_storage=100,
    # NOTE: For production, use a larger instance type.
    # Last checked price: $0.1590 per hour = ~$110 per month
    db_instance_class="db.m6g.large",
    availability_zone=ws_settings.aws_az1,
    db_subnet_group=prd_airflow_db_subnet_group,
    enable_performance_insights=True,
    aws_secret=prd_airflow_db_secret,
    skip_delete=skip_delete,
    save_output=save_output,
)

# -*- Airflow Elasticache Redis Cluster
prd_airflow_redis_cluster = CacheCluster(
    name=f"airflow-redis-{ws_settings.prd_key}",
    enabled=use_elasticache,
    engine="redis",
    num_cache_nodes=1,
    # NOTE: For production, use a larger instance type.
    # Last checked price: $0.068 per hour = ~$50 per month
    cache_node_type="cache.t2.medium",
    cache_subnet_group=prd_airflow_redis_subnet_group,
    preferred_availability_zone=ws_settings.aws_az1,
    skip_delete=skip_delete,
    save_output=save_output,
)

# -*- ResourceGroup for airflow AWS resources
prd_airflow_aws_resources = ResourceGroup(
    name="airflow",
    enabled=ws_settings.prd_airflow_enabled,
    resources=[
        prd_airflow_db_volume,
        prd_airflow_redis_volume,
        prd_airflow_db_subnet_group,
        prd_airflow_redis_subnet_group,
        prd_airflow_db_secret,
        prd_airflow_rds_db,
        prd_airflow_redis_cluster,
    ],
)
