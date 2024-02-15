from __future__ import annotations

import os
import configparser
from pathlib import Path
import toml


def get_dev_config(
    environment: str = 'dev', # toml file section
    app_config_path: Path = Path.cwd().joinpath('app.toml'), # create path to toml file from host dir
) -> dict:
    try:
        app_config = toml.load(app_config_path) # load the toml file as dictionary
        config = configparser.ConfigParser(inline_comment_prefixes="#")
        # read the contents of snowsql/config file into config
        if app_config['snowsql_config_path'].startswith('~'):
            a  = config.read(os.path.expanduser(app_config['snowsql_config_path']))
        else:
            a = config.read(app_config['snowsql_config_path'])
        # get credentials from config file (title = connections.dev)
        session_config = config[
            'connections.' +
            app_config['snowsql_connection_name']
        ]
        session_config_dict = {
            k.replace('name', ''): v.strip('"')
            for k, v in session_config.items()
        }
        # update session details ( login etc) with db / schema for the deployment
        session_config_dict.update(app_config.get(environment))  # type: ignore
        return session_config_dict
    except Exception:
        raise Exception(
            "Error creating snowpark session - be sure you've logged into "
            "the SnowCLI and have a valid app.toml file",
        )
