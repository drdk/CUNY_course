# CUNY_course

_<center>Cuny_Course</center>_

## 📚 Documentation

For detailed information on how to use this project, **[click here](https://drdk.github.io/CUNY_course/)** ✨ to check out the official documentation.

### Methods
TODO


### Examples
```python
TODO
```


---

!!! note
    The project is inspired by [cookiecutter-hypermodern-python][insp-repo]

[insp-repo]: https://github.com/cjolowicz/cookiecutter-hypermodern-python

## Project structure

The project is structured the following way

```
├── .vscode
├── CUNY_course
├── data
├── docs
├── jobs
├── notebooks
├── scripts
├── tests
├── tools
├── .flake8
├── .gitignore
├── .pre-commit-config.yaml
├── mkdocs.yml
├── noxfile.py
├── poetry.lock
├── pyproject.toml
├── README_dev.md
└── README.md
```

## Local development

!!! info
    The project requires that you've installed [Poetry] to manage python dependencies and [pre-commit] for automated issue detection prior git commits.
    
To install `poetry` follow [the official installation guidelines](https://python-poetry.org/docs/#installation).
Start by running the following command that will create a new virtual environment and install all packages required as specified in `pyproject.toml`

```zsh
poetry install
```

Next run `pre-commit` install to set up the git hook scripts. **Note**: pre-commit asserts that git version control has been initiated.

```zsh
pre-commit install
```

Activate the virtual environment by running

```zsh
poetry shell
```

When you want to leave the virtual environment created by poetry you just execute

```zsh
deactivate
```

## Execute CUNY_course from console

The CUNY_course-package can be executed from commandline, evoking the package `__main__`.

```zsh
poetry run CUNY_course
```


## Nox - A pythonic Makefile

`nox` is command-line tool that automates testing in multiple python environments, but the library can also be used to generate a pythonic approach to makefiles. The project uses `nox` as the single entrypoint to do everything from testing, serving docs.

!!!info
    Learn more about `nox` by visiting their great [documentation ](https://nox.thea.codes)

The following sessions are defined:

- `init git repo` - Uses git and the GitHub CLI to init a local and remote github [repository]
- `build docs` - The following session will build the docs and the API documentation using [MkDocs]. They can be found in the directory `site/`. [codecov] will report on test coverage
- `format checking` - Check that python code and notebooks follows the [Black] and [Prettier] standards
- `format` - Fix anti patterns, format-checking and imports
- `import checking` - Checks that all imports are correctly sorted and follows the black and [isort] standard
- `lint checking` - Flag anti patterns in python with [Flake8]
- `serve docs` - serve docs on localhost:8000
- `safety checking` - performs security audit on used libraries with [safety] 
- `type checking` - Check that your type annotations are consistent with [mypy]
- `unit tests` - Run unit tests in current environment with [pytest]
- `unit tests - venv` - Run unit tests across python versions locally
- `create release` - Creates a new release at the github [repository]

Given the poetry .venv is active, a `nox`-session is activated using the folling pattern:

```zsh
nox -s "<session name>"
```

!!! warning
    If no session is specified (executing `nox` without the `-s` option) the following session will be executed. `format checking`, `import checking`, `lint checking`, `type checking`, `safety checking` and `unit tests`


[black]: https://github.com/psf/black
[click]: https://click.palletsprojects.com/
[codecov]: https://codecov.io/
[coverage.py]: https://coverage.readthedocs.io/
[flake8]: http://flake8.pycqa.org
[isort]: https://pycqa.github.io/isort/
[mypy]: http://mypy-lang.org/
[myst]: https://myst-parser.readthedocs.io/
[nox]: https://nox.thea.codes/
[poetry]: https://python-poetry.org/
[pre-commit]: https://pre-commit.com/
[prettier]: https://prettier.io/
[pytest]: https://docs.pytest.org/en/latest/
[safety]: https://github.com/pyupio/safety
[MkDocs]: https://www.mkdocs.org/
[repository]: https://github.com/drdk/CUNY_course
