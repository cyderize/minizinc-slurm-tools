# MiniZinc SLURM Tools

Tools for analysing [minizinc-slurm](https://github.com/Dekker1/minizinc-slurm) results.

## Installation

```sh
pip install git+https://github.com/cyderize/minizinc-slurm-tools
```

This will make the `mznst` CLI tool available.

## Command-line tool

### Checking solutions

The `check-solutions` command takes the solutions output during run and feeds them back into
the model to check that the result is satisfiable. It also stores the objective and satisfiability
information to be used when checking statuses. The `-c` option can be used to set how many solutions
to check (zero to check all solutions)

```sh
mznst check-solutions -c 3 ./results
```

### Checking statuses

The `check-statuses` command takes the results from `check_solutions` plugin (which must be
run first) and then checks for any solvers which have either
- Falsely claimed optimality - where optimality was found by a solver,
  but a better objective was found elsewhere and verified to be correct.
- Falsely claimed unsatisfiability - where unsatisfiability was found by a solver, 
  but another solver has given a correct solution for the instance.

```sh
mznst check-statuses ./results
```

### Collecting results as CSV

For further processing of data (e.g. using [pandas](https://pandas.pydata.org/) or
[R](https://www.r-project.org/)) it may be useful to save the objective and statistics data to CSV.
This can be done using the `collect-results` command. The actual solutions are not saved, only the
objective values achieved.

```sh
mznst collect-results ./results objective_output.csv statistics_output.csv
```

## Working with the data

The `read_csv` function from `mznst.analysis.collect` can be used to read the objective and
statistics CSV output into a tuple of pandas data frames.

### Plotting figures

There are a number of plotting helper functions available in `mznst.analysis.plot`.
These use the [Bokeh](https://bokeh.org/) visualisation library to provide interactive plots.

```py
from mznst.analysis.collect import read_csv
from mznst.analysis.plot import plot_all_instances
from bokeh.plotting import show

sols, stats = read_csv("objective_output.csv", "statistics_output.csv")
show(plot_all_instances(sols, stats))
```

### Summary analysis statistics

TBD.
