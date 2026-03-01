import os
from typing import List


class MissingEnvironmentVariable(Exception):
    """
    Exception used to report errors in loading environment variables.
    Raised when an expected environment variable is not set, providing a clear
    and informative message about which variable is missing.
    """


def validate_env_variables(env_names: List[str]) -> None:
    """
    Validates whether the required environment variables are set.

    This function checks a list of environment variable names and validates
    each one using os.getenv. If any environment variable is not found,
    it raises an exception indicating which variable is missing.

    Args:
        env_names (List[str]): The names of the environment variables to validate.

    Raises:
        MissingEnvironmentVariable: If any environment variable is not set
            in the environment.
    """
    for var_name in env_names:
        if os.getenv(var_name) is None:
            raise MissingEnvironmentVariable(
                f"{var_name} not found in environment variables"
            )
