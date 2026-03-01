# Developer guide

<!-- links -->

[admonitions]: https://squidfunk.github.io/mkdocs-material/reference/admonitions/#supported-types
[pre-commit]: https://pre-commit.com/
[flake8]: http://flake8.pycqa.org
[mypy]: http://mypy-lang.org/
[coverage.py]: https://coverage.readthedocs.io/
[semver]: https://semver.org/
[conventionalcommits]: https://www.conventionalcommits.org/en/v1.0.0/
[nox]: https://nox.thea.codes/
[orgs/drdk]: [https://github.com/drdk]
[pytest]: https://docs.pytest.org/en/latest/

<!-- links end -->

## Working with the .venv

### Configure Poetry to use the pyenv Python version

First, make sure that you've set the global Python version using `pyenv`. You can check the global Python version by running

```zsh
pyenv global
```

When creating a new virtual environment, `Poetry` will, by default, use the Python version available in the environment where it’s run. Since you've set the global Python version using `pyenv`, you can tell `Poetry` to use this version.

To ensure Poetry uses the same Python version managed by `pyenv`, you can create the virtual environment using the specific Python interpreter:

```zsh
poetry env use $(pyenv which python)
```

This command explicitly tells Poetry to use the Python interpreter provided by `pyenv`.

## Installing dependencies from drdk-github

### Locally

Ensure you have installed the GitHub CLI as this will allow you to configure authentication to the drdk-github organization [orgs/drdk]

```zsh
brew install gh
```

Once installed you authenticate your DR GitHub user. Follow the guide when entering:

```zsh
gh auth login
```

**Note**: An easy choice is to use:
- GitHub.com
- HTTPS
- GitHub credentials
- Paste an authentication token

From here you simply add packages using `poetry` as usually:

```zsh
poetry add git+https://github.com/drdk/<PACKAGE_NAME>.git
```

### On the pipeline

#### Create PAT

On the pipeline, `CircleCI` needs a Github access token to be able to install packages.

One of such (a personal access token) can be generated [here](https://github.com/settings/tokens).

!!! note SSO
    SSO needs to be configured for that token.

This access token needs the following scopes:

- repo: Full control of private repositories 
- write:packages: Upload packages to GitHub Package Registry

#### Add in CircleCI
Next add this access token as an environment variable in `CircleCI` at:
https://app.circleci.com/settings/project/github/drdk/CUNY_course/environment-variables

For simplicity give the token the following name; **ACCESS_TOKEN**

#### Modify pipeline build

In order to make this secret available doing build-time, the file `.circleci/config.yml` needs modification.
<br>
Replace this:

```yml
# Jobs / Build And Publish / steps / run
  command: |
    dockercli --publish
```

with this:

```yml
# Jobs / Build And Publish / steps / run
  command: |
    dockercli --build-args ACCESS_TOKEN=$ACCESS_TOKEN --publish
```

Because we set the **ACCESS_TOKEN** secret as an env. variable doing in the Dockerfile, and we configure `git` to use it when `poetry` is calling repos in the drdk-github organization, dependencies can now be installed on the pipeline.

## Testing

### Fixtures

In [pytest], the _scope_ of a fixture determines how often the fixture is set up and torn down during a test session. By default, fixtures in pytest have a function scope. This means the fixture is invoked and a new instance is created for each test function that requests it. However, pytest allows several other scopes for fixtures: class, module, package, and session.

```python
# tests/conftest.py
@pytest.fixture(scope="module")
def standard_data_row() -> Dict[str, Any]:
    (...)
```

Here's a brief explanation of each scope:

- **Function** (default): The fixture is created anew for each test function. This is the most common and default scope, ensuring that no state persists between tests.
- **Class**: The fixture is created once for each test class. All test methods in the class can use the same fixture instance.
- **Module**: The fixture is created once per test module, regardless of how many test functions or classes are in the module. Useful when several tests in a module share heavy setup but do not modify the setup.
- **Package**: The fixture is created once per package (a directory of test modules), ideal for sharing a more extensive setup across multiple modules in a package.
- **Session**: The fixture is created only once per test session. This is useful for very expensive setup steps that need to occur only once throughout the entire testing session, such as launching or connecting to external resources.

## Creating releases

Given a version number MAJOR.MINOR.PATCH, increment the:

- MAJOR version when you make incompatible API changes, that breaks previous implementation.
- MINOR version when you add functionality and features in a backward compatible manner
- PATCH version when you make backward compatible bug fixes.

This guide is defined as by [semver] and [conventionalcommits]

*Note*: the [nox] command-line `create release` creates a new release at the github repo

## Workarounds in the project template

At it's core `nox`is intended to be an great asistance by automating testing, linting, type checking among others. However, sometimes workarrounds is needed.

### git commit

The `--no-verify` flag can be used with git commit to bypass the [pre-commit][pre-commit] hooks set in your project. This is helpful when you need to make commits without the interference of hooks, such as when the hooks are producing false positives or when a commit is urgent and there isn't time to address all hook checks. Note that skipping hooks should be used sparingly as it bypasses important checks designed to maintain code quality.

```zsh
git commit -m "Commit message" --no-verify
```

This command will commit changes to your repository without executing any pre-commit hooks configured in `.git/hooks/pre-commit`.

### flake8

The `# noqa:`-comment can be used to disable specific [flake8] warnings for a particular line. This is useful when you need to intentionally violate a style rule for clarity or due to limitations in the tool's ability to interpret complex code scenarios.

```python
import os  # noqa: F401
```

### mypy

```# type: ignore``` This comment tells [mypy] to ignore type checks for a given line. It's particularly useful when integrating with external libraries that might not be fully type-hinted or when using constructs that are known to confuse the type checker.

```python
result = some_function()  # type: ignore
```

### codecov

`# pragma: no cover` This comment instructs the code coverage tools [coverage.py][coverage.py] to ignore the line for coverage reporting. This is useful for code that is difficult or impractical to test in an automated test environment.

```python
def my_function():
    if False:  # pragma: no cover
        print("This won't be executed")
```

## Making documentation

### Admonitions

Admonitions, also known as *call-outs*, are an excellent choice for including side content without significantly interrupting the document flow. Material for MkDocs provides several different types of admonitions and allows for the inclusion and nesting of arbitrary content. 

Syntax examples could be:
- !!! note (regular block)
- ??? note (colabsible block)
- !!! warning "New title" (Change title)
- !!! note "" (no tille)

For usage and more examples go [here][admonitions].

### Logo and favicon

Current favicon: ![Favicon](docs/assets/favicon.png)

go to ```docs/assets/favicon.png``` to replace it.

Current logo:

<img alt="logo" src="docs/assets/logo.svg" width="50%" />

go to ```docs/assets/logo.svg``` to replace it.

