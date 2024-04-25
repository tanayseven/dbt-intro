import os
import sys
from pathlib import Path

import jinja2
import yaml
from yaml import load

python_path = os.environ.get("PYTHONPATH")
if not python_path:
    print("PYTHONPATH not set, please set it and re-run the script.")
    sys.exit(1)
yaml_file = (Path(python_path) / "dbt_intro" / "profiles.yml").read_text()
print(yaml_file)
dbt_profile = load(yaml_file, yaml.Loader)
dbt_default_profile = dbt_profile['dbt_intro']['outputs']['default-target']
alembic_variables = dict(
    driver="snowflake",
    user=f"{dbt_default_profile['user']}",
    password=f"{dbt_default_profile['password']}",
    account=f"{dbt_default_profile['account']}",
    database=f"{dbt_default_profile['database']}",
    schema=f"{dbt_default_profile['schema']}",
)
raw_alembic_file_content = (Path.cwd() / "alembic.raw.ini").read_text()
rendered_alembic_file = Path.cwd() / "alembic.ini"
rendered_file_content = jinja2.Template(raw_alembic_file_content).render(alembic_variables)

override_file = True
if rendered_alembic_file.exists():
    valid = {"yes": True, "y": True, "ye": True, "": True, "no": False, "n": False}
    response = input("File already exists, override it? (Y/n)").lower()
    if response not in valid:
        print("Invalid response")
        exit(1)
    override_file = valid[response]
    if not override_file:
        exit(0)
rendered_alembic_file.write_text(rendered_file_content)
