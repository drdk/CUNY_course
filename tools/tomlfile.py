from pathlib import Path
import toml
from typing import List, Any, Dict

from tools.navigating import get_project_root


def load_toml_file(file_path: str = "pyproject.toml") -> Any:
    """
    Load and return the contents of a TOML file.

    Args:
        file_path (str): The path to the TOML file. Defaults to pyproject.toml, the
            project env. file.

    Returns:
        Any: The parsed TOML file as a dictionary.
    """
    return toml.load(Path(file_path))


class PyprojectToml:
    """
    A class to represent and interact with the pyproject.toml file in a project.

    Attributes:
        toml (Any): The contents of the pyproject.toml file parsed as a dictionary.
    """

    def __init__(self) -> None:
        """Initialize the PyprojectToml class and read the pyproject.toml file."""
        self.toml_path = Path(get_project_root(), "pyproject.toml")
        self.toml: Any = self.__read_toml()

    def __read_toml(self) -> Any:
        """
        Read and load the pyproject.toml file.

        Returns:
            Any: The parsed contents of the pyproject.toml file as a dictionary.
        """
        return load_toml_file(self.toml_path)

    @property
    def poetry(self) -> Dict[str, Any]:
        """
        Get the poetry section of the pyproject.toml file.

        Returns:
            Dict[str, Any]: The poetry section as a dictionary.
        """
        return self.toml.get("tool", {}).get("poetry", {})

    @property
    def name(self) -> str:
        """
        Get the project name from the poetry section.

        Returns:
            str: The project name.
        """
        return self.poetry.get("name", "")

    @property
    def version(self) -> str:
        """
        Get the project version from the poetry section.

        Returns:
            str: The project version.
        """
        return self.poetry.get("version", "")

    @version.setter
    def version(self, new_version: str) -> None:
        """
        Set a new project version in the pyproject.toml file and reload it.

        Args:
            new_version (str): The new version to set.
        """
        assert self.poetry

        # Read the file as text
        with open(self.toml_path, "r") as file:
            lines = file.readlines()

        # Modify only the line containing the version
        with open(self.toml_path, "w") as file:
            version_line_prefix = 'version = "'
            for line in lines:
                if line.strip().startswith(version_line_prefix):
                    # Replace the existing version with the new version
                    old_version = line.strip().split('"')[1]
                    line = line.replace(old_version, new_version)
                file.write(line)

        self.toml = self.__read_toml()

    @property
    def description(self) -> str:
        """
        Get the project description from the poetry section.

        Returns:
            str: The project description.
        """
        return self.poetry.get("description", "")

    @property
    def authors(self) -> List[str]:
        """
        Get the list of authors from the poetry section.

        Returns:
            List[str]: The list of authors.
        """
        return self.poetry.get("authors", [])

    @property
    def authors_as_dict(self) -> Dict[str, str]:
        """
        Get the list of authors as a dictionary with names as keys and emails as values.

        Returns:
            Dict[str, str]: The authors as a dictionary.
        """
        authors = {}
        for author in self.authors:
            idx = author.find("<")
            authors[author[: idx - 1]] = author[idx:]
        return authors

    @property
    def maintainers(self) -> List[str]:
        """
        Gives the github user-name of all of the project maintainers.

        Returns:
            List[str]: The github username of all maintainers
        """
        return self.poetry.get("maintainers", [])

    @property
    def packages(self) -> List[Dict[str, str]]:
        """Get the list of package dependencies.

        Returns:
            List[Dict[str, str]]: All package dependencies
        """
        return self.poetry.get("packages", [{}])

    @property
    def repository(self) -> str:
        """Get the repository url.

        Returns:
            str: The url to the project repository
        """
        return self.poetry.get("repository", "")
