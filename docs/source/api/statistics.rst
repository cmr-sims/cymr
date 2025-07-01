Statistics
==========

.. currentmodule:: cymr.statistics

Statistic definitions are used to define a set of statistical analyses that
may be used to fit a model. Definitions for a set of analyses are stored in 
a  :py:class:`Statistics` object, which defines analyses to be run, not the
results of analyses. :py:class:`Statistics` objects may be used to evaluate
statistics on a given dataset.

Statistic definitions may be saved to a JSON file to document exactly what 
statistics were fitted, in a form that can be loaded and reused.

Statistic definitions
~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
    :toctree: api/

    Statistics
    Statistics.set_stat
    Statistics.eval_stats
    Statistics.compare_stats

Analysis definitions
~~~~~~~~~~~~~~~~~~~~

.. autosummary

Statistic definition files
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
    :toctree: api/

    Statistics.to_json
    read_json
