from pathlib import Path
from typing import List, Optional, Union
from dataclasses import dataclass
import pandas as pd
from ruamel.yaml import YAML

yaml = YAML(typ="unsafe")


def collect_dataframe(
    dirs: List[Union[str, Path]], filter_stats: Optional[List[str]] = None
):
    base_keys = ["configuration", "problem", "model", "data_file", "time"]
    solutions = []
    statistics = []
    for dir in dirs:
        path = (dir if isinstance(dir, Path) else Path(dir)).resolve()
        for file in path.rglob("*_sol.yml"):
            with file.open() as fp:
                sols = yaml.load(fp)
                for sol in sols or []:
                    if "solution" not in sol:
                        continue
                    obj = sol["solution"].get("objective", None)
                    solution = {k: sol[k] for k in base_keys}
                    solution["objective"] = obj
                    solution["run"] = path.name
                    solutions.append(solution)

        for file in path.rglob("*_stats.yml"):
            with file.open() as fp:
                stats = yaml.load(fp)
                if filter_stats is not None:
                    stats = {k: stats[k] for k in base_keys + filter_stats}
                stats["run"] = path.name
                statistics.append(stats)

    return pd.DataFrame(solutions), pd.DataFrame(statistics)

def read_csv(sols: str, stats: str):
    sols_df = pd.read_csv(sols)
    stats_df = pd.read_csv(stats)
    sols_df.data_file = sols_df.data_file.fillna('')
    stats_df.data_file = stats_df.data_file.fillna('')
    return sols_df, stats_df
