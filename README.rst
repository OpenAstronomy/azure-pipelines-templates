**************************************
OpenAstronomy Azure Pipeline Templates
**************************************

This repository contains set of templates for `Azure Pipelines
<https://azure.microsoft.com/en-gb/services/devops/pipelines/>`_ that helps
simplify configuration in individual packages. At this time, there are two main
templates available - one to make it easy to map `tox
<https://tox.readthedocs.org>`__ environments to builds on Azure Pipelines, and
one to automate the process of releasing Python packages.

Loading the templates
=====================

Set up a GitHub service connection
----------------------------------

The first step to using the templates is to set up a GitHub service connection.
To do this, go to the Azure configuration for the repository where you want to
use the templates. Then click on **Project Settings** (in the bottom left as of
2019-09-18), then go to the **Service connections** section in the settings.

If a GitHub service connection already exists, note its name down, otherwise
create one. We suggest giving it a general name such as your username or the
GitHub organization name.

Loading the template in your Azure configuration
------------------------------------------------

To load the template, add the following to the beginning of the ``azure-pipelines.yml``:

.. code:: yaml

    resources:
      repositories:
      - repository: OpenAstronomy
        type: github
        endpoint: <service connection name>
        name: OpenAstronomy/azure-pipelines-templates
        ref: master

where ``<service connection name>`` is the name of the service connection you
set up above. This will make the templates in this repository available in the
``OpenAstronomy`` namespace in the rest of the file. Note the ref allows you to
pin the template version you want, you can use ``master`` if you want the latest
version.

Tox template
============

This template borrows heavily from `tox's templates <https://github.com/tox-dev/azure-pipelines-template>`__.

You must have a ``tox.ini`` and a ``azure-pipelines.yml`` file in your main repository.
Then for each job you want to run, you have to create a entry for it within your ``azure-pipelines.yml`` file.

Example
-------

.. code:: yaml

    jobs:
    - template: run-tox-env.yml@sunpy
      parameters:
        name: Linux_37_offline
        os: macos
        tox: py37-offline -- -n=4

This example will run the ``py37-offline`` on Linux.
Here ``py37-offline`` is the name of a tox environment that is in the SunPy's `tox.ini`.

Th parameters are:

* ``name`` : Name of the build.
* ``os``: The operating system to use - ``windows``, ``macos``, ``linux``.
* ``tox`` : The name of the tox environment as well as any extra inputs to pytest.

Python package release template
===============================

This template automates the process of building wheels as well as a source
distribution, and uploading them all to PyPI. Your project must be PEP-517 and
PEP-518 compatible in order to use this.

Configuring the PyPI service connection
---------------------------------------


Usage and options
-----------------

To make use of this template, add the following to the ``azure-pipelines.yml`` file:

.. code:: yaml

    jobs:
    - template: publish@OpenAstronomy
      parameters:
        pypi_remote: 'test'
        targets:
        - sdist
        - wheels_linux
        - wheels_macosx
        - wheels_windows

``pypi_remote`` should be set to the name of the PyPI service connection you set
up above, and ``targets`` should be set to a list of builds you want to generate
- the four options are shown in the example above (wheels for the three main
platforms and a source distribution) but you can choose to only build some of
these if you want. The initial ``if`` statement ensures that this process is only

If you want to run tests on the generated packages (which we recommend), you can make use of
the following parameters:

.. code:: yaml

    jobs:
    - template: publish@OpenAstronomy
      parameters:
        pypi_remote: 'test'
        test_extras: "all,test"
        test_command: pytest --pyargs sunpy
        targets:
        ...

Here ``test_extras`` is the list of extras_requires options that will be used
when installing the built package for testing - these are options that are
typically specified using the following syntax: ``pip install package[all,test]``.
The ``test_command`` parameter gives a command that will be run in a temporary
directory and has to rely on the installed version of the package (hence the use
of ``--pyargs`` in the example above).

The wheel building process is carried out by `cibuildwheel
<https://github.com/joerick/cibuildwheel>`_, and can be customized using all the
environment variables supported by that package. For example, you can place the
following at the top of your ``azure-pipelines.yml`` file to force wheels to only
be built on Python 3.6 and 3.7, and excluding 32-bit Windows and Linux.

.. code:: yaml

    variables:
      CIBW_BUILD: cp36-* cp37-*
      CIBW_SKIP: "*-win32 *-manylinux1_i686"
