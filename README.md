# MiniZinc SLURM Tools

Tools for analysing [minizinc-slurm](https://github.com/Dekker1/minizinc-slurm) results.

## Installation

```sh
pip install git+https://github.com/cyderize/minizinc-slurm-tools
```

## Checking solutions

The `check_solutions` PyTest plugin takes the solutions output during run and feeds them back into
the model to check that the result is satisfiable. It also stores the objective and satisfiability
information to be used when checking statuses.

```sh
pytest -p mznst.pytest.check_solutions ./results
```

## Checking statuses

The `check_statuses` pytest plugin takes the results from `check_solutions` plugin (which must be
run first) and then checks for any solvers which have either
- Falsely claimed optimality - where optimality was found by a solver,
  but a better objective was found elsewhere and verified to be correct.
- Falsely claimed unsatisfiability - where unsatisfiability was found by a solver, 
  but another solver has given a correct solution for the instance.

```sh
pytest -p mznst.pytest.check_statuses ./results
```
