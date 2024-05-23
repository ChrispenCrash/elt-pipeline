from datetime import datetime
from airflow import DAG
from docker.types import Mount  # type: ignore
from airflow.utils.dates import days_ago  # type: ignore
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator  # type: ignore
from airflow.providers.docker.operators.docker import DockerOperator  # type: ignore

CONN_ID = "<replace with Airbyte connection ID>"

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
}


dag = DAG(
    "elt_and_dbt",
    default_args=default_args,
    description="An ELT workflow with dbt",
    start_date=datetime(2024, 5, 19),
    catchup=False,
)

t1 = AirbyteTriggerSyncOperator(
    task_id="airbyte_postgres_postgres",
    airbyte_conn_id="airbyte",
    connection_id=CONN_ID,
    asynchronous=False,
    timeout=3600,
    wait_seconds=3,
    dag=dag,
)

t2 = DockerOperator(
    task_id="dbt_run",
    image="ghcr.io/dbt-labs/dbt-postgres:1.7.14",
    command=[
        "run",
        "--profiles-dir",
        "/root",
        "--project-dir",
        "/dbt",
        "--full-refresh",
    ],
    auto_remove=True,
    docker_url="unix://var/run/docker.sock",
    network_mode="bridge",
    mounts=[
        Mount(
            source="/home/chris/elt-pipeline/postgres_transformations",
            target="/dbt",
            type="bind",
        ),
        Mount(source="/home/chris/.dbt", target="/root", type="bind"),
    ],
    dag=dag,
)

t1 >> t2
