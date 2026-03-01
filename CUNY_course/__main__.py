"""Command-line interface."""

import click


@click.command()  # transforms the function into a command-line command.
@click.version_option()  # adds a --version option to the CLI command
def main() -> None:
    """Cuny_Course."""
    msg: str = "Now running CUNY_course. Expected more? Go to __main__.py"
    click.echo(msg)


if __name__ == "__main__":
    # 'no cover' : exclude line from code coverage statistics
    main(prog_name="CUNY_course")  # pragma: no cover
