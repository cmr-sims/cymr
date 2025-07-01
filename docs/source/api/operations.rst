Operations
==========

.. py:module:: cymr.operations

    Cython code to simulate network mechanisms.

The :py:mod:`operations` module contains Cython code designed to run
core CMR mechanisms as fast as possible. Mechanisms operate on
:py:class:`~cymr.network.Network` objects.

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
