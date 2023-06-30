# Product Injuries Data Pipeline

## Architecture of the pipeline

![Architecture Diagram](/docs/architecture.png)


## DBT Lineage


## Data Sources
- [Injuries](https://data.world/awram/us-product-related-injuries)
- [Product Codes Mapping](https://public.opendatasoft.com/explore/dataset/us-national-electronic-injury-surveillance-system-neiss-product-codes/export/?refine.code=0102)


## Setup

1. Setup and start Airbyte: [docs](https://docs.airbyte.com/deploying-airbyte/local-deployment/#setup--launch-airbyte). [TODO: Export config from AirByte].
2. Create virtualenv and install the dependencies with `pdm install`.
3. Start MinIO & Postgres with `docker compose up`.
4. Add the following config to your ~/.dbt/profiles.yml:
    ```
    product_injuries:
      target: dev
      outputs:
        dev:
          type: postgres
          host: localhost
          user: <dbt_postgres_user>
          password: <dbt_postgres_password>
          port: 54320
          dbname: injuries
          schema: public
          threads: 1
    ```
5. Start the local orion server or connect to [Prefect Cloud](https://docs.prefect.io/2.10.18/cloud/cloud-quickstart/).
6. Set all the required env variables:
    ```
    MINIO_ACCESS_KEY
    MINIO_SECRET_KEY
    ```
7. [TODO] Dashboard & API.
8. [TODO] CICD with GitHub Actions.