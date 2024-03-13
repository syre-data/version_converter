# %%
import os
import json
from glob import glob

from . import paths, common


# %%
def convert_project_scripts(base_path: str):
    """Convert project .syre/scripts.json to .syre/analyses.json.
    Adds entry ["type": "script"] for each script.

    Args:
        path (str): Path to project folder.
    """
    from_path = os.path.join(base_path, paths.SYRE_FOLDER, "scripts.json")
    analyses_path = paths.project_analyses_of(base_path)
    if  os.path.exists(from_path) and not os.path.exists(analyses_path):
        os.rename(from_path, analyses_path)

    with open(analyses_path, "r+") as f:
        analyses = json.load(f)
        for analysis in analyses:
            if "type" not in analysis:
                analysis["type"] = "Script"


def convert_container_associations(container_properties_path: str):
    """Renames `container.scripts` to `container.analyses`.

    Args:
        container_properties_path (str): Path to the container's properties file.
    """
    with open(container_properties_path, "r+") as f:
        container = json.load(f)
        if "scripts" in container:
            container["analyses"] = container.pop("scripts")
        else:
            container["analyses"] = []

        f.seek(0)
        json.dump(container, f, indent=4)
        f.truncate()


def convert_all_containers(project_path: str):
    """Converts all the Containers in a project from 0.10.1 to 0.10.2.

    Args:
        project_path (str): Path to the project's root.
    """
    data_path = common.project_data_path(project_path)
    glob_pattern = os.path.join(data_path, "**", paths.container_properties())
    for container_properties_path in glob(glob_pattern, recursive=True):
        convert_container_associations(container_properties_path)


def convert(project: str):
    """Converts the project located at the given path from 0.10.1 to 0.10.2.

    Args:
        project (str): Path to the project.
    """
    convert_project_scripts(project)
    convert_all_containers(project)

