from typing import Callable
import argparse

from . import common
from . import convert_0_10_1

VERSIONS = [
    "0.10.1",
    "0.10.2"
]

CONVERTERS = {
    "0.10.1": convert_0_10_1.convert
}

def convert_chain(initial: str, final: str) -> list[Callable]:
    """Creates a chain of converters

    Args:
        initial (str): Initial version.
        final (str): Final version.
        
    Returns:
        list[Callable]: List of callables to convert from initial to final version.
    """
    try:
        initial_idx = VERSIONS.index(initial)
    except ValueError:
        raise ValueError("Invalid initial verison")
    
    try:
        final_idx = VERSIONS.index(final)
    except ValueError:
        raise ValueError("Invalid final version")
    
    return [CONVERTERS[version] for version in VERSIONS[initial_idx:final_idx]]
    

parser = argparse.ArgumentParser(
    prog="Syre version converter",
    description="Converts Syre projects between version.",
)

parser.add_argument("initial", help="Current version. (x.y.z)")
parser.add_argument("final", help="Final version. (x.y.z)")
parser.add_argument("--project", "-p", help="Only convert the project at the given path.")

args = parser.parse_args()
convert_chain = convert_chain(args.initial, args.final)
if len(convert_chain) == 0:
    raise ValueError("No conversion to perform.")

if args.project is None:
    for project in common.project_paths():
        for convert in convert_chain:
            convert(project)
else:
    for convert in convert_chain:
        convert(args.project)
