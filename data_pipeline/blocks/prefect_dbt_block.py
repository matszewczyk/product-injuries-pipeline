from prefect_dbt.cli.configs import PostgresTargetConfigs
from prefect_dbt.cli import DbtCliProfile, DbtCoreOperation

postgres_target_configs = PostgresTargetConfigs.load("dbt-product-injuries")

dbt_cli_profile = DbtCliProfile(
    name="product_injuries",
    target="dev",
    target_configs=postgres_target_configs
)
dbt_cli_profile.save("dbt-cli-profile", overwrite=True)

dbt_cli_profile = DbtCliProfile.load("dbt-cli-profile")
dbt_core_operation = DbtCoreOperation(
    commands=["dbt build"],
    profiles_dir="~/.dbt/",
    project_dir="~/product_injuries_project/dbt/",
    # dbt_cli_profile=dbt_cli_profile,
    # overwrite_profiles=True,
)
dbt_core_operation.save("dbt-build-block", overwrite=True)
