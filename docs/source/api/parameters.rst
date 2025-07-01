Parameters
==========

.. py:module:: cymr.parameters

    Management of model parameters.

.. currentmodule:: cymr.parameters

Parameter definitions are used to define free and fixed parameters and the
allowable ranges of free parameters. They may also be used to define
dependent parameters that are defined in terms of other parameters and
dynamic parameters that vary based on the data being fitted. 

Parameter definitions are stored in :py:class:`Parameters` objects. 
They should not be confused with parameter dictionaries, which only 
contain specific parameter values, but no metadata.

:py:class:`Parameters` may be saved to a JSON file to document the 
parameter definitions of a model variant, in a form that can be loaded 
and reused.

Search parameters
~~~~~~~~~~~~~~~~~

.. autosummary::
    :toctree: api/

    Parameters
    Parameters.set_fixed
    Parameters.set_free

Dependent parameters
~~~~~~~~~~~~~~~~~~~~

.. autosummary::
    :toctree: api/

    Parameters.set_dependent
    Parameters.eval_dependent

Dynamic parameters
~~~~~~~~~~~~~~~~~~

.. autosummary::
    :toctree: api/

    Parameters.set_dynamic
    Parameters.eval_dynamic

Parameter sets
~~~~~~~~~~~~~~

.. autosummary::
    :toctree: api/

    Parameters.copy
    Parameters.to_json
    read_json
