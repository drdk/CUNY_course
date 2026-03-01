import glob
import subprocess
import sys
import tempfile
from configparser import ConfigParser
from pathlib import Path

import nox
from nox_poetry import Session, session
from packaging.version import parse as parse_version

from tools.color import Color
from tools.docfix import collect_modules_for_documentation
from tools.navigating import get_project_root
from tools.tomlfile import PyprojectToml


CODE_DIRS = ["noxfile.py", "CUNY_course", "scripts", "tests"]
IGNORE = ["tools"]
NOTEBOOK_DIRS = ["notebooks"]
CODE_DIRS_WITH_NOTEBOOKS = CODE_DIRS + NOTEBOOK_DIRS
DEFAULT_PYTHON_VERSION = False
DEFAULT_VENV_BACKEND = "none"
MINIMAL_CODE_COVERAGE = 80
PYTHON_VERSIONS = ["3.9", "3.10", "3.11"]


# Specify default tasks
nox.options.sessions = (
    "format checking",
    "import checking",
    "lint checking",
    "type checking",
    "safety checking",
    "unit tests",
)


@session(name="init git repo")
def init_git_repo(session: Session) -> None:
    """
    Initialize the local directory as a Git repository and set up a remote repository
    if not already configured.

    Args:
        session (Session): _description_
    """
    # Check if git already exists
    git_status = subprocess.run(["git", "status"], capture_output=True, text=True)
    if git_status.stderr.strip():
        # Initiate git versioning
        try:
            session.run("git", "init", "-b", "main", external=True)
            session.run("git", "add", ".", external=True)
            session.run(
                "git", "commit", "-m", "first commit", "--no-verify", external=True
            )
            session.log("Git repository initialized and initial commit made.")
        except Exception as e:
            session.error(f"Failed to initialize Git repository: {e}")
    else:
        session.log("Git versioning already initiated")

    # Check if remote is set
    git_remote = subprocess.run(["git", "remote"], capture_output=True, text=True)
    if not git_remote.stdout.strip():
        # Initiate remote repo
        toml_file = PyprojectToml()
        try:
            session.run(
                "gh",
                "repo",
                "create",
                f"drdk/{toml_file.name}",
                "--internal",
                external=True,
            )
            session.run("git", "remote", "add", "origin", f"{toml_file.repository}")
            session.run("git", "push", "-u", "origin", "main")
            session.log(f"Remote repository drdk/{toml_file.name} created and linked.")
        except Exception as e:
            session.error(f"Failed to set up remote repository: {e}")
    else:
        session.error("A remote repository has already been configured")

    # Create and push 'test' branch
    try:
        session.run("git", "checkout", "-b", "test", external=True)
        session.run("git", "push", "-u", "origin", "test", external=True)
        session.log("Created and pushed 'test' branch.")
    except Exception as e:
        session.error(f"Failed to create and push 'test' branch: {e}")

    # Install pre-commit hooks
    session.run("pre-commit", "install", external=True)


@session(
    name="format",
    python=DEFAULT_PYTHON_VERSION,
    venv_backend=DEFAULT_VENV_BACKEND,
)
def format(session: Session) -> None:
    """
    Automatically format code using autoflake, black and isort
    """
    session.run("autoflake", "--recursive", *CODE_DIRS)
    session.run("black", *CODE_DIRS_WITH_NOTEBOOKS)
    session.run("isort", *CODE_DIRS)


@session(
    name="format checking",
    python=DEFAULT_PYTHON_VERSION,
    venv_backend=DEFAULT_VENV_BACKEND,
)
def code_format_checking(session: Session) -> None:
    """
    Checks format checking using black
    """
    session.run("black", "--check", *CODE_DIRS_WITH_NOTEBOOKS)


@session(
    name="import checking",
    python=DEFAULT_PYTHON_VERSION,
    venv_backend=DEFAULT_VENV_BACKEND,
)
def import_checking(session: Session) -> None:
    """
    Checks import formatting using isort with black profile
    """
    session.run("isort", "--check-only", *CODE_DIRS)


@session(
    name="lint checking",
    python=DEFAULT_PYTHON_VERSION,
    venv_backend=DEFAULT_VENV_BACKEND,
)
def lint_checking(session: Session) -> None:
    """
    Lints code using flake8
    """
    session.run("flake8", *CODE_DIRS)


@session(
    name="type checking",
    python=DEFAULT_PYTHON_VERSION,
    venv_backend=DEFAULT_VENV_BACKEND,
)
def type_checking(session: Session) -> None:
    """
    Checks type information using mypy
    """
    args = session.posargs or CODE_DIRS
    args = [arg for arg in args if not any(arg.startswith(f"{dir}") for dir in IGNORE)]
    args.append("noxfile.py") if not args else None
    session.run(
        "mypy",
        "--no-strict-optional",
        "--ignore-missing-imports",
        f"--python-executable={sys.executable}",
        *args,
    )


@session(
    name="unit tests",
    python=DEFAULT_PYTHON_VERSION,
    venv_backend=DEFAULT_VENV_BACKEND,
)
def current_environment(session: Session) -> None:
    """
    Runs unit testing using pytest with required coverage
    """
    unit_test(session)


@session(name="unit tests - venv", python=PYTHON_VERSIONS)
def all_environment(session: Session) -> None:
    """
    Runs unit testing using pytest with required coverage
    """
    session.run_always("poetry", "install", external=True)
    unit_test(session)


def unit_test(session: Session) -> None:
    session.run(
        "pytest",
        "--cov=CUNY_course",
        "--cov-report",
        "html",
        f"--cov-fail-under={MINIMAL_CODE_COVERAGE}",
        "-n",
        "auto",
        *session.posargs,
    )


@session(
    name="safety checking",
    python=DEFAULT_PYTHON_VERSION,
    venv_backend=DEFAULT_VENV_BACKEND,
)
def safety_checking(session: Session) -> None:
    """
    Runs package safety checking using safety
    """
    config = ConfigParser()
    safety_ignore_file = Path(get_project_root(), ".safety")
    ignored_issues = ""
    if safety_ignore_file.exists():
        config.read(safety_ignore_file)
        if "safety" in config and "ignore" in config["safety"]:
            ignored_issues = config["safety"]["ignore"].strip()
            ignore_flag = f"--ignore={ignored_issues}"
    else:
        ignore_flag = ""

    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--with",
            "dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        session.run(
            "safety",
            "check",
            f"--file={requirements.name}",
            "--full-report",
            ignore_flag,
        )


@session(
    name="build docs",
    python=DEFAULT_PYTHON_VERSION,
    venv_backend=DEFAULT_VENV_BACKEND,
)
def build_docs(session: Session) -> None:
    """
    Builds documentation using mkdocs
    """
    collect_modules_for_documentation(dest_file=Path("./docs/api.md"))
    session.run("mkdocs", "build")


@session(
    name="serve docs",
    python=DEFAULT_PYTHON_VERSION,
    venv_backend=DEFAULT_VENV_BACKEND,
)
def serve_docs(session: Session) -> None:
    """
    Serves documentation using mkdocs
    """
    session.run("mkdocs", "serve", *session.posargs)


@session(
    name="clean notebook outputs",
    python=DEFAULT_PYTHON_VERSION,
    venv_backend=DEFAULT_VENV_BACKEND,
)
def clean_notebook_outputs(session: Session) -> None:
    """
    Cleans all notebook prints in .ipynb files
    """
    notebook_files = [
        file
        for notebook_dir in NOTEBOOK_DIRS
        for file in glob.glob(f"{notebook_dir}/**/*.ipynb", recursive=True)
    ]
    session.run(
        "jupyter",
        "nbconvert",
        "--clear-output",
        "--to",
        "notebook",
        *notebook_files,
    )


@session(name="create release")
def create_release(session: Session) -> None:
    """
    Creates a new release at the github repo
    """
    # Check if the current branch is 'main'
    branch_result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True
    )
    current_branch = branch_result.stdout.strip()
    if current_branch != "main":
        session.error(
            f"Incorrect branch: {current_branch}. Switch to 'main' and try again."
        )

    # Check for unstaged changes
    changes = subprocess.run(
        ["git", "status", "--porcelain"], capture_output=True, text=True
    )
    if changes.stdout.strip():
        session.error("There are unstaged changes. Commit or stash before deploying")

    # Load the current project version from pyproject.toml
    toml_file = PyprojectToml()
    session.log(f"Current version: {toml_file.version}")
    session.log(
        f"{Color.Y}NB: If you haven’t already authenticated your GitHub CLI "
        "installation, you need to log in first. "
        f"Use `gh auth login` {Color.RESET}"
    )
    # Prompt for a new version
    new_version = input(
        f"{Color.R}Enter new version (press enter to abort): {Color.RESET}"
    )
    if new_version:
        if parse_version(new_version) <= parse_version(toml_file.version):
            session.error("New version must be higher than the current version.")

        toml_file.version = new_version
        session.log(f"New version: {toml_file.version}")

        # Stage changes and commit
        session.run("git", "add", "pyproject.toml", external=True)

        msg: str = f"Update version to {new_version}"
        session.run("git", "commit", "-m", msg, "--no-verify", external=True)

        msg = f"Release version {new_version}"
        session.run("git", "tag", "-a", f"v{new_version}", "-m", msg, external=True)

        session.run("git", "push", "origin", f"v{new_version}", external=True)
        session.run(
            "gh",
            "release",
            "create",
            f"v{new_version}",
            "--generate-notes",
            external=True,
        )
        session.run("git", "push")
        session.run("mkdocs", "gh-deploy")

        # Commit updated site files if any changes are present
        site_changes = subprocess.run(
            ["git", "status", "--porcelain", "site"], capture_output=True, text=True
        )
        if site_changes.stdout.strip():
            session.log("Committing updated site files after mkdocs gh-deploy...")
            session.run("git", "add", "site", external=True)
            try:
                session.run(
                    "git",
                    "commit",
                    "-m",
                    "Update site files after mkdocs gh-deploy",
                    external=True,
                )
                session.run("git", "push", external=True)
            except Exception as e:
                session.error(f"Failed to commit site changes: {e}")

        # Final step: Update only the pyproject.toml file in the test branch
        try:
            session.log("Updating pyproject.toml in 'test' branch from 'main'...")
            # Switch to the test branch
            session.run("git", "checkout", "test", external=True)
            # Update pyproject.toml by checking out its version from main
            session.run(
                "git", "checkout", "main", "--", "pyproject.toml", external=True
            )
            # Stage the updated file
            session.run("git", "add", "pyproject.toml", external=True)
            # Commit the update if there are changes
            session.run(
                "git",
                "commit",
                "-m",
                f"Update pyproject.toml version to {new_version} from main",
                external=True,
            )
            # Push the changes to the test branch
            session.run("git", "push", "origin", "test", external=True)
            session.log("Successfully updated 'test' branch with new pyproject.toml.")
        except Exception as e:
            session.error(f"Failed to update 'test' branch: {e}")
        finally:
            # Ensure we return to the main branch
            session.run("git", "checkout", "main", external=True)
    else:
        session.error("Aborting version update")