"""
Converts a Syre project from version 0.10.2 to 0.11.0.

# Config
+ Changes `users.json` from object to list.

# Projects
+ Moves `creator` and `created` fields into settings.

# Containers
+ Moves `creator` and `created` fields into settings.
"""
import json
import logging

from . import paths

logger = logging.getLogger(__name__)

def convert_config():
    """Converts `users.json` from an object to a list.
    """
    with open(paths.config_project_manifest(), "r+") as f:
        users = json.load(f)
        users = [user for (_, user) in users.items()]
        f.seek(0)
        json.dump(users, f, indent=4)
        f.truncate()

def convert_project_properties(base_path: str):
    """Converts the Project from 0.10.2 to 0.11.0.
    Moves `creator` and `created` fields into settings.

    Args:
        base_path (str): Path to the project's root.
    """
    raise NotImplementedError()


def convert_all_containers(project_path: str):
    """Converts all the Containers in a project from 0.10.2 to 0.11.0.
    Moves `creator` and `created` fields into settings.

    Args:
        project_path (str): Path to the project's root.
    """
    raise NotImplementedError()



def convert(project: str):
    """Converts the project located at the given path from 0.10.2 to 0.11.0.

    Args:
        project (str): Path to the project.
    """
    logger.info("[0.10.2]")
    convert_config()
    convert_project_properties(project)
    convert_all_containers(project)

