CMR
===

.. py:module:: cymr.cmr

    Tools for implementing variants of the context maintenance 
    and retrieval model (CMR).

.. currentmodule:: cymr.cmr

The :py:mod:`~!cymr.cmr` module provides tools for implementing various CMR
model variants using the :py:class:`CMR` class. Rather than implementing 
one specific version of CMR, :py:class:`CMR` is designed to be highly 
configurable via changes to the :py:class:`CMRParameters` class, which 
supports various ways of defining network weights and parameter values.

Model variants may be evaluated against observed data by calculating
likelihood, or fitted to data using a parameter search. They can also be
used to generate simulated data.

Model variants are defined by :py:class:`CMRParameters` objects, which
may be saved to JSON files, and patterns, which are stored in HDF5 format.
The patterns define representations associated with individual items. The
patterns may be orthonormal, as in the original implementations of TCM and
CMR, or they may be overlapping, as in DCMR. :py:class:`CMRParameters`
specify how patterns are used to determine weights in the network, among
other model settings.

Model framework
~~~~~~~~~~~~~~~

.. autosummary::
    :toctree: api/

    CMR
    CMR.likelihood
    CMR.fit_indiv
    CMR.generate
    CMR.record
    CMR.parameter_sweep
    CMR.parameter_recovery

Model configuration
~~~~~~~~~~~~~~~~~~~

.. autosummary::
    :toctree: api/

    save_patterns
    load_patterns
    read_config
    config_loc_cmr

Model parameters
~~~~~~~~~~~~~~~~

.. autosummary::
    :toctree: api/

    CMRParameters
    CMRParameters.set_fixed
    CMRParameters.set_free
    CMRParameters.set_dependent
    CMRParameters.eval_dependent
    CMRParameters.set_dynamic
    CMRParameters.eval_dynamic
    CMRParameters.set_sublayers
    CMRParameters.set_weights
    CMRParameters.set_sublayer_param
