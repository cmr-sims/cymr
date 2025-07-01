Operations
==========

The :py:mod:`operations` module contains Cython code designed to run
core CMR mechanisms as fast as possible.

.. currentmodule:: cymr.operations

Basic operations
~~~~~~~~~~~~~~~~

.. autosummary::
    :toctree: api/

    integrate
    present
    cue_item
    apply_softmax

Simulating tasks
~~~~~~~~~~~~~~~~

.. autosummary::
    :toctree: api/

    study
    study_distract
    p_recall
