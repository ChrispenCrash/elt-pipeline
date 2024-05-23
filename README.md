# ELT Data Pipeline

This repository contains a custom Extract, Load, Transform (ELT) project that utilizes Docker, PostgreSQL, dbt, Airflow and Airbyte to demonstrate a simple ELT process. The ELT process involves extracting data from a source PostgreSQL database, loading it into a destination PostgreSQL database using Airflow and Airbyte, then transforming/modelling the data using dbt. <br>
This project was made by following along with the great [video](https://www.youtube.com/watch?v=PHsC_t0j1dU&list=PLp9B-SYXR0uNU940Q_Sn7Zx4ekRz3UD4z) on Data Engineering by Justin Chau.

## Requirements
- Docker

## Repository Structure

1. **docker-compose.yaml**: This file contains the configuration for Docker Compose, which is used to orchestrate multiple Docker containers. It defines five services:
   - `source_postgres`: The source PostgreSQL database.
   - `destination_postgres`: The destination PostgreSQL database.
   - `init-airflow`: The service that initializes Airflow.
   - `webserver`: The service that runs the Airbyte webserver.
   - `scheduler`: The service that runs the Airbyte scheduler.

2. **source_db_init/init.sql**: This SQL script initializes the source database with sample data. It creates tables for users, films, film categories, actors, and film actors, and inserts sample data into these tables.

## Getting Started

### Initial Setup

1. Run airbyte/run-ab-platform.sh to start Airbyte.
2. Airbyte should start at `localhost:8000` with username: airbyte password: password. Create a new connection between the source and destination databases and set the schedule to manual, we will use Airflow to trigger the sync.
3. Grab the Airbyte connection ID from the URL and use it to replace the `<replace with Airbyte connection ID>` in the `airflow/dags/elt_dag.py` file.
4. Initialize Airflow using `docker compose up init-airflow`, wait for a few seconds and then run `docker compose up -d`. This will run all the remaining services.
5. Inside the Airflow UI, a new connection will have to be added. Use the following details:
   - Connection Id: `airbyte`
   - Connection Type: `HTTP`
   - Host: `host.docker.internal`
   - Login: `airbyte`
   - Password: `password`
   - Port: `8001`
6. The ELT DAG should now work in the Airflow UI.
7. Use `./end.sh` to stop all services.

### Running the ELT Process

1. Run `./start.sh`, this will first initialize Airflow, then start the remaining services, including Airbyte.