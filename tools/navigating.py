from pathlib import Path


def get_project_root(marker="pyproject.toml") -> Path:
    """
    Finds the project's root directory by searching for a marker file using pathlib.

    Parameters:
        marker (str): The name of the marker file to look for.

    Returns:
        Path: The path to the project root directory.

    Raises:
        FileNotFoundError: If the marker file is not found up to the root of the
            filesystem.
    """
    current_dir = Path.cwd()
    for parent in [current_dir] + list(current_dir.parents):
        if (parent / marker).exists():
            return Path(parent)
    raise FileNotFoundError(
        f"Marker file '{marker}' not found in any parent directories."
    )
