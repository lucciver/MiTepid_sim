MiTepid_sim
===========

.. image:: https://img.shields.io/pypi/v/mitepid.svg
    :target: https://pypi.python.org/pypi/mitepid
    :alt: Latest PyPI version
.. image:: https://img.shields.io/badge/License-GPLv3-blue.svg
   :target: https://www.gnu.org/licenses/gpl-3.0

Usage
-----
MiTepid_sim: A repository to simulate the spread of COVID19. 

This code simulates a set of nonlinear ODEs which can simulate the spread of a virus in any population with a known age structure, using both SIR and SIS models. The parameters of this model are estimated based on the available data on the spread of COVID-19. The details of that method, which relies on an optimisation scheme, are explained in the manuscript. The optimisation itself is done using the GLobal Optimisation Toolbox in Matlab. But the optimised values of the model parameters are uploaded with this code. Hence the code should work well under Python 3. There is a script coming with the code called ``script_main.py`` which can be used as a template for how to run the code, and demonctrstaes its capabilities. 

Updates on the model and how it can be used to predict the spread of COVID-19 can be found in:
https://people.tuebingen.mpg.de/vbokharaie/ 

Installation
------------
In your command prompt or bash, simply type:

 .. code-block:: bash

    pip install mitepid

Or you can install it from repo if you want to have the latest (untested) updates. 

Basic Usage
-----------
In the following code, it is assumed that CVODI-19 has a spread of 1 in 10,000 in all age groups in Germany. The disease spreads uncontained for 60 days and then various containment policies are imposed and the resulting plots for each case saved under ``sample_outputs`` subfolder in current working directory. 

 .. code-block:: bash

    from mitepid.func_main import main

    from pathlib import Path
    subfolder = Path('sample_outputs')
    dir_save_plots_main = Path(Path.cwd(), subfolder)
    country = 'Germany'
    t_end = 541
    list_t_switch = [0, 60]
    policy_list = ['Uncontained',
                   'Schools_closed',
                   'Elderly_self_isolate',
                   'Kids_Elderly_self_isolate',
                   'Schools_Offices_closed',
                   'Adults_Elderly_Self_isolate',
                   'Social_Distancing',
                   'Lockdown',
                   ]

    for policy in policy_list:
        all_policies = ['Uncontained',]
        all_policies.append(policy)
        policy_definition = dict(zip(list_t_switch, all_policies))
        x00 = 1e-4  # initial condition
        x0_vec=[x00, x00, x00, x00, x00, x00, x00, x00, x00,]
        policy_name = 'Uncontained_then_' + policy
        print('*********************************************')
        print(policy_name)
        dict_current = main(country, policy_name, policy_definition,
                            dir_save_plots_main, t_end=t_end, x0_vec=x0_vec)


Requirements
^^^^^^^^^^^^

 .. code-block:: python

    numpy
    scipy
    matplotlib


Compatibility
-------------

This code is tested under Python 3.8, and should work well for all current versions of Python 3.

Licence
-------
GNU General Public License (Version 3).


Author
-------

`MiTepid` is maintained by `Vahid Samadi Bokharaie <vahid.bokharaie@tuebingen.mpg.de>`_.
