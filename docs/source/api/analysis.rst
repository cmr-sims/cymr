Analysis
========

.. py:module:: cymr.analysis

    Specification of analyses that can be used to evaluate model fit.

.. currentmodule:: cymr.analysis

Statistic definitions are used to define a set of statistical analyses that
may be used to fit a model. Definitions of individual analyses are stored 
in :py:class:`Analysis` objects, which specify how an analysis should be 
run and the expected output variables.

Definitions for a set of analyses are stored in a :py:class:`Statistics`
object. :py:class:`Statistics` objects may be used to evaluate
statistics on a given dataset, and can be used with 
:py:func:`~cymr.cmr.CMR.fit_indiv` to fit parameters to specific statistics,
rather than overall likelihood.

Statistic definitions may be saved to a JSON file to document exactly what 
statistics were fitted, in a form that can be loaded and reused.

Analysis definitions
~~~~~~~~~~~~~~~~~~~~

.. autosummary::
    :toctree: api/

    Analysis
    Analysis.eval

Statistic definitions
~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
    :toctree: api/

    Statistics
    Statistics.set_stat
    Statistics.eval_stats
    Statistics.compare_stats

Statistic definition files
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
    :toctree: api/

    Statistics.to_json
    read_json
