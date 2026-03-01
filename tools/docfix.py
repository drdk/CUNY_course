from pathlib import Path
from tools.tomlfile import PyprojectToml


def _write_to_api_file(
    base_path: Path,
    package_name: str,
    dest_file: Path,
) -> None:
    """
    Write documentation for a package to the output file.

    Args:
        base_path (Path): The base directory path where the package directories are
            located.
        package_name (str): The package information, including its name.
        dest_file (Path): The file to write the documentation to.
    """
    package_path = base_path / package_name

    if package_path.exists() and package_path.is_dir():
        with dest_file.open("a") as f:
            f.write(f"# {package_name} - API\n\n")
            for python_script in package_path.rglob("*.py"):
                if python_script.stem != "__init__":
                    module_path = ".".join(python_script.parts).replace(".py", "")
                    f.write(f"::: {module_path}\n")


def collect_modules_for_documentation(dest_file: Path = Path(".docs/api.md")) -> None:
    """
    Generate documentation based on package information in a TOML file.

    Args:
        dest_file (Path): The path to the output markdown file for documentation.
    """
    packages = PyprojectToml().packages

    # Ensure the docs directory exists and clear the contents of the file
    dest_file.parent.mkdir(parents=True, exist_ok=True)
    dest_file.write_text("")

    for package in packages:
        _write_to_api_file(
            Path("."), package_name=package.get("include", ""), dest_file=dest_file
        )
