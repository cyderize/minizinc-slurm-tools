from typing import Any, Dict
import random
import click
import pytest
from minizinc import Model, Solver, Status
from minizinc.helpers import check_solution
from ruamel.yaml import YAML

yaml = YAML(typ="unsafe")


class SolFile(pytest.File):
    checker: Solver
    num_check: int

    def __init__(self, checker: Solver, num_check: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.checker = checker
        self.num_check = num_check

    def collect(self):
        with self.fspath.open() as fp:
            results = yaml.load(fp) or []
            pairs = [
                (i, result) for i, result in enumerate(results) if "solution" in result
            ]
            if len(pairs) == 0:
                return
            if self.num_check is None:
                # Check every solution
                check = range(len(pairs))
            else:
                # Sample random solutions to check, but always include final one
                n = len(pairs) - 1
                check = [n] + random.choices(range(n), k=min(n, self.num_check - 1))
            for i in sorted(check):
                num, result = pairs[i]
                name = ":".join(
                    (
                        result["configuration"],
                        result["problem"],
                        result["model"],
                        result["data_file"],
                        str(num),
                    )
                )
                yield SolItem.from_parent(
                    self, name=name, result=result, checker=self.checker
                )


class SolItem(pytest.Item):
    result: Dict[str, Any]
    checker: Solver
    key: str

    def __init__(self, result: Dict[str, any], checker: Solver, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result = result
        self.checker = checker
        self.key = "{}_{}_{}".format(
            self.result["problem"], self.result["model"], self.result["data_file"]
        )
        self.config.cache.set("obj/" + self.key, (None, None))
        self.config.cache.set("sat/" + self.key, False)

    def runtest(self):
        # Check solution
        solution: Dict[str, Any] = self.result["solution"]
        model = Model(self.result["model"])
        model["mzn_ignore_symmetry_breaking_constraints"] = True
        model["mzn_ignore_redundant_constraints"] = True
        if "data_file" in self.result and len(self.result["data_file"]) > 0:
            model.add_file(self.result["data_file"])
        status = Status[self.result["status"]]
        assert check_solution(
            model, solution, status, self.checker
        ), "Incorrect solution"

        # Record that the problem is satisfiable for use in check_statuses
        self.config.cache.set("sat/" + self.key, True)

        # Record objective bounds for use in check_statuses
        objective = solution.get("objective", None)
        if objective is not None:
            min_obj, max_obj = self.config.cache.get("obj/" + self.key, (None, None))
            if min_obj is None or objective < min_obj:
                min_obj = objective
            if max_obj is None or objective > max_obj:
                max_obj = objective
            self.config.cache.set("obj/" + self.key, [min_obj, max_obj])

    def reportinfo(self):
        return self.fspath, 0, "usecase: {}".format(self.name)


class ConfTest:
    checker: Solver
    num_check: int

    def __init__(self, check: int) -> None:
        self.checker = Solver.lookup("gecode")
        self.num_check = check if check > 0 else None

    def pytest_collect_file(self, parent, path):
        if path.basename.endswith("_sol.yml"):
            return SolFile.from_parent(
                parent, fspath=path, checker=self.checker, num_check=self.num_check
            )


@click.command()
@click.option(
    "-c",
    "--check",
    default=1,
    help="Number of solutions to check per instance (randomly chooses which, but always checks final solution).",
)
@click.argument("dir")
def main(dir: str, **kwargs):
    pytest.main([dir], plugins=[ConfTest(**kwargs)])
