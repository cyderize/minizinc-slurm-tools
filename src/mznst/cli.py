from typing import Iterable
import click
import pytest
from .analysis.collect import collect_dataframe

@click.group()
def main():
    """Command-line tools for processing and analysing minizinc-slurm results."""
    pass


@main.command()
@click.option(
    "-c",
    "--check",
    default=1,
    help="""Number of solutions to check per instance
            (randomly chooses which, but always checks final solution).
            Setting to zero will check all solutions.
            """,
)
@click.argument("dir", nargs=1)
@click.argument("pytest_args", nargs=-1)
def check_solutions(check: int, dir: str, pytest_args: Iterable[str]):
    """Checks the correctness of solutions produced during a minizinc-slurm run.

    This is done by feeding the solution produced back into the model and checking
    that is is still satisfiable.

    \b
    DIR is the directory containing YAML output from minizinc-slurm
    PYTEST_ARGS are passed to the underlying PyTest command
    """
    args = ["-p", "mznst.pytest.check_solutions", "--check", str(check), dir]
    args.extend(pytest_args)
    exit(pytest.main(args))


@main.command()
@click.argument("dir", nargs=1)
@click.argument("pytest_args", nargs=-1)
def check_statuses(dir: str, pytest_args: Iterable[str]):
    """Checks for incorrect proof of optimality/unsatisfiability.

    This can only be run after the check-solutions command has been run.

    \b
    DIR is the directory containing YAML output from minizinc-slurm
    PYTEST_ARGS are passed to the underlying PyTest command
    """
    args = ["-p", "mznst.pytest.check_statuses", dir]
    args.extend(pytest_args)
    exit(pytest.main(args))


@main.command()
@click.argument("dirs", nargs=-1)
@click.argument("sols_file", nargs=1)
@click.argument("stats_file", nargs=1)
def collect_results(dirs: Iterable[str], sols_file: str, stats_file: str):
    """Collects all results as CSV for later use.

    \b
    DIRS are directories containing the result YAML files
    SOLS_FILE is the output CSV file containing objective data
    STATS_FILE is the output CSV file containing statistics data
    """
    sols, stats = collect_dataframe(list(dirs))
    sols.to_csv(sols_file)
    stats.to_csv(stats_file)
