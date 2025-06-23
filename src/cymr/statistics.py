"""Manage statistical measures."""

import importlib
import pandas as pd


class Analysis(object):
    """Manage analysis specification."""

    def __init__(
        self, 
        call,
        independent,
        dependent,
        level,
        args=None, 
        kwargs=None, 
        conditions=None,
    ):
        self.callable = call
        self.args = args if args is not None else []
        self.kwargs = kwargs if kwargs is not None else {}
        self.independent = independent
        self.dependent = dependent
        self.conditions = conditions
        self.level = level
    
    def __repr__(self):
        fields = [
            "callable", 
            "args", 
            "kwargs", 
            "independent", 
            "dependent", 
            "conditions", 
            "level",
        ]
        d = {f: getattr(self, f) for f in fields}
        s = "\n".join([f"{key}={val}" for key, val in d.items()])
        return s
    
    def eval(self, data):
        """Evaluate an analysis on a dataset."""
        # get the callable to run
        mod, fun = self.callable.split(":")
        f = getattr(importlib.import_module(mod), fun)

        if self.conditions is not None:
            # apply the analysis to each cond
            res = data.groupby(self.conditions).apply(
                f, *self.args, **self.kwargs, include_groups=False
            )
            res.index = res.index.droplevel(-1)
            res = res.reset_index().convert_dtypes()

            if self.level == "group":
                # average over subjects
                res = res.groupby(
                    self.independent + self.conditions
                )[self.dependent].mean().reset_index()
            
            # get the group labels and values
            conds = res[self.conditions].apply(
                lambda df: ",".join(df.values.astype(str)), axis=1
            )
            cond_vars = ",".join(self.conditions)
        else:
            # apply the analysis to the whole dataset
            res = f(data, *self.args, **self.kwargs)
            conds = "n/a"
            cond_vars = "n/a"
            if self.level == "group":
                res = res.groupby(
                    self.independent
                )[self.dependent].mean().reset_index()
        
        if self.level == "group":
            subject = "n/a"
            independent_cols = self.independent
        else:
            subject = res["subject"].astype(str)
            independent_cols = self.independent

        # get the dependent variable        
        y = res[self.dependent]

        # get independent variable names and values
        independent = res[independent_cols].apply(
            lambda df: ",".join(df.values.astype(str)), axis=1
        )
        names = ",".join(independent_cols)

        # package results in a standardized condensed data frame
        stat = pd.DataFrame(
            {
                "condition_vars": cond_vars,
                "conditions": conds,
                "subject": subject,
                "independent_vars": names,
                "independent": independent,
                "dependent_var": self.dependent,
                "dependent": y
            }
        )
        return stat, res


class Statistics(object):

    def __init__(self, error_stat="rmsd", weighting="point"):
        self.error_stat = error_stat
        self.weighting = weighting
        self.stats = {}

    def __repr__(self):
        parts = {}
        for name in ["error_stat", "weighting", "stats"]:
            obj = getattr(self, name)
            if isinstance(obj, dict):
                fields = [f"\n{key}:\n{value}" for key, value in obj.items()]
                parts[name] = "\n".join(fields)
            else:
                parts[name] = obj
        s = "\n\n".join([f"{name}:\n{f}" for name, f in parts.items()])
        return s
    
    def set_stat(self, stat, *args, **kwargs):
        """Configure an analysis to generate a statistic."""
        self.stats[stat] = Analysis(*args, **kwargs)
    
    def eval_stats(self, data):
        """Evaluate all statistics."""
        results = {}
        stat_list = []
        for stat_name, stat_def in self.stats.items():
            stat, res = stat_def.eval(data)
            stat["stat"] = stat_name
            stat_list.append(stat)
            results[stat_name] = res
        stats = pd.concat(stat_list, ignore_index=True)
        return stats, results
