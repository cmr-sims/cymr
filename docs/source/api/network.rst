Network
=======

.. currentmodule:: cymr.network

The :py:mod:`network` module includes efficient functions for running
core mechanisms of CMR. These functions will generally not be called
directly by users. See the :py:mod:`~cymr.cmr` module for high-level functions
for running parameter searches and simulations using CMR.

Network Initialization
~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
    :toctree: api/

    Network

Accessing and Setting Values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
    :toctree: api/

    Network.copy
    Network.reset
    Network.get_sublayer
    Network.get_sublayers
    Network.get_segment
    Network.get_unit
    Network.add_pre_weights

Operations
~~~~~~~~~~

.. autosummary::
    :toctree: api/

    Network.update
    Network.integrate
    Network.present
    Network.learn

Simulating Tasks
~~~~~~~~~~~~~~~~

.. autosummary::
    :toctree: api/

    Network.study
    Network.p_recall
    Network.generate_recall
    Network.generate_recall_lba

Recording and Visualization
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
    :toctree: api/

    Network.record_study
    Network.record_recall
    Network.plot
