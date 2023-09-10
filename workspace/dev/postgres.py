from phi.docker.app.postgres import PostgresDb

from workspace.settings import ws_settings

# -*- Run a postgres database on docker

# -*- Postgres running on port 8315:5432
dev_postgres_app = PostgresDb(
    name="postgres-dp",
    enabled=ws_settings.dev_db_enabled,
    db_user="dp",
    db_password="dp",
    db_schema="dp",
    # Airflow uses the postgresql:// connection string
    db_driver="postgresql",
    # Connect to this db on port 8315
    container_host_port=8315,
)

# -*- Postgres connection ids for airflow
dev_postgres_connection_id = "postgres"
dev_postgres_airflow_connections = {
    dev_postgres_connection_id: dev_postgres_app.get_db_connection()
}
