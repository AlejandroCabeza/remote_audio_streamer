# Python Imports
# Third-Party Imports
# Project Imports


class EnvironmentVariableNotFound(Exception):

    def __init__(self, environment_variable_key: str):
        message: str = f"Environment variable '{environment_variable_key}' not found."
        super().__init__(message)
