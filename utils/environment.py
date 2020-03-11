# Python Imports
from typing import Any
from os import environ
# Third-Party Imports
# Project Imports
from infrastructure.exceptions import EnvironmentVariableNotFound


def get_environment_variable_or_error(key: str) -> Any:
    try:
        return environ[key]
    except KeyError:
        raise EnvironmentVariableNotFound(key)
