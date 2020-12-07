# MiniZinc SLURM Tools

Tools for analysing [minizinc-slurm](https://github.com/Dekker1/minizinc-slurm) results.

## Installation

```sh
pip install git+https://github.com/cyderize/minizinc-slurm-tools
```

## Checking solutions

The `check_solutions` script takes the solutions output during run and feeds them back into the
model to check that the result is satisfiable.

```sh
check_solutions ./results
```

## Checking statuses

The `check_statuses` script takes the results from `check_solutions` (which must be run first)
and then checks for any solvers which have falsely claimed optimality (i.e. where optimality was
found by a solver, but a better objective was found elsewhere and verified to be correct).

```sh
check_statuses ./results
```
