MiTepid_sim
===========

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

If you are using Anaconda on Windows, better to open an Anaconda command prompt
and then type the above.

Or if you want to work with the latest beta-release, you can find it in:

https://gitlab.tuebingen.mpg.de/vbokharaie/mitfat


    **If you don't know anything about Python:**

    then you should not worry. In order to use this code, you do not need to know anything about python. You just need to install it and then follow the instructions in the Usage Section to be able to run the code. But you need to install Python first. Python is just a programming language and unlike Matlab is not owned by a company or organization, hence you do not need to bu a license to use it. There are various ways to install Python, but the easiest is to go `here <https://docs.conda.io/en/latest/miniconda.html>`_ and install Miniconda Python 3.x (3.7 at the time of writing). This will install Python and a minimal set of commonly used libraries (Libraries in Python are equivalent to toolboxes in Matlab). A little detail to keep in mind for Windows users is that you need to open an Anaconda Prompt (which you can find in your Start menu) and then type ``pip install mitepid`` to install the MitfAT library. Typing it in a normal windows command prompt (which you can open by typing ``cmd`` in 'Search program or file' in Start menu) might not work properly.

    When Python is installed, then follow the instructions below to use this code to analyse your fMRI data. I should add though, that I sincerely hope using this code can motivate you to learn a bit about Python. I learned how to use Matlab 20 years ago and still use it to this day. But as I learn more about Python and what is available in this ecosystem, I use Matlab less and Python more and more every day. Python provides powerful tools for you that you did not know you are missing when you were writing programs in Matlab. If you want to learn the basics of Python, I can suggest this `online book <https://jakevdp.github.io/PythonDataScienceHandbook/>`_ to start with.


Basic Usage
-----------

To understand what the code does, please look at `this manuscript <http://people.tuebingen.mpg.de/vbokharaie/pdf_files/Quantifying_COVID19_Containment_Policies.pdf>`_. 


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


Authors
-------

`MiTepid` is maintained by `Vahid Samadi Bokharaie <vahid.bokharaie@tuebingen.mpg.de>`_.
