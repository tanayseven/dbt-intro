from pathlib import Path

import typer
import jinja2

app = typer.Typer()

@app.command(
    name="create",
    help="Create configs",
)
def main(
        snowflake_account: str = typer.Option(..., help="Snowflake account"),
        snowflake_user: str = typer.Option(..., help="Snowflake user"),
        snowflake_password: str = typer.Option(..., help="Snowflake password"),
):
    jinja2_env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="config_templates"))

    snowflake_creds_template = jinja2_env.get_template("snowflake_creds.json")
    rendered = snowflake_creds_template.render(
        snowflake_account=snowflake_account,
        snowflake_user=snowflake_user,
        snowflake_password=snowflake_password,
    )
    creds_file = Path.cwd() / "airflow" / "dags" / "snowflake_creds.json"
    creds_file.write_text(rendered)

    snowflake_profiles_yaml_template = jinja2_env.get_template("profiles.yml")
    rendered = snowflake_profiles_yaml_template.render(
        snowflake_account=snowflake_account,
        snowflake_user=snowflake_user,
        snowflake_password=snowflake_password,
        query_tag="AIRFLOW_AUTOMATION",
    )
    profiles_file = Path.cwd() / "airflow" / "dags" / "profiles.yml"
    profiles_file.write_text(rendered)



