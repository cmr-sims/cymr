Fit
===

.. py:module:: cymr.fit

    Tools for fitting models to free-recall data.

.. currentmodule:: cymr.fit

The :py:mod:`~!cymr.fit` module provides tools for fitting a model to 
free-recall data. Models can inherit from the :py:class:`Recall` class and 
implement subject-level methods for evaluating likelihood and simulating
data. The model class will then have access to high-level methods for 
evaluating, fitting, and simulating models.

Utilities
~~~~~~~~~

.. autosummary::
    :toctree: api/

    prepare_lists
    prepare_study
    get_best_results
    add_recalls

Model evaluation
~~~~~~~~~~~~~~~~

.. autosummary::
    :toctree: api/

    Recall
    Recall.likelihood_subject
    Recall.likelihood

Parameter estimation
~~~~~~~~~~~~~~~~~~~~

.. autosummary::
    :toctree: api/

    Recall.fit_subject
    Recall.fit_indiv

Generating simulated data
~~~~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
    :toctree: api/

    Recall.generate_subject
    Recall.generate

Characterizing model parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
    :toctree: api/

    Recall.parameter_sweep
    Recall.parameter_recovery
