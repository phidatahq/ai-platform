from phi.aws.resource.s3 import S3Bucket
from phi.resource.group import ResourceGroup

from workspace.settings import ws_settings

#
# -*- S3 buckets for the Production Environment
#

# -*- S3 bucket for storing logs
prd_logs_s3_bucket = S3Bucket(
    name=f"{ws_settings.prd_key}-logs",
    acl="private",
    skip_delete=False,
    save_output=True,
)
# -*- S3 bucket for storing data
prd_data_s3_bucket = S3Bucket(
    name=f"{ws_settings.prd_key}-data",
    acl="private",
    skip_delete=False,
    save_output=True,
)

# -*- ResourceGroup for production S3 buckets
prd_s3_buckets = ResourceGroup(
    name="s3",
    resources=[prd_data_s3_bucket, prd_logs_s3_bucket],
)
