**************************************
OpenAstronomy Azure Pipeline Templates
**************************************

This repository contains set of templates for `Azure Pipelines
<https://azure.microsoft.com/en-gb/services/devops/pipelines/>`_ that helps
simplify configuration in individual packages. At this time, there are two main
templates available - one to make it easy to map `tox
<https://tox.readthedocs.org>`__ environments to builds on Azure Pipelines, and
one to automate the process of releasing Python packages.

The templates in this repository were inspired and adapted from `tox's
<https://github.com/tox-dev/azure-pipelines-template>`__ and `SunPy's templates
<https://github.com/sunpy/azure-pipelines-template>`_.

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

The purpose of this template is to make it easy to map `tox
<https://tox.readthedocs.io/>`__ environments to Azure jobs. To use this
template, your repository will need to have a ``tox.ini`` file.

Basic setup
-----------

To use this template, you will need to add the following section to your
``azure-pipelines.yml`` file:

.. code:: yaml

    jobs:
    - template: run-tox-env.yml@OpenAstronomy
      parameters:
        envs:
        - <os>: <tox env>
        - <os>: <tox env>

Where ``<os>`` is the operating system to test on, and ``<tox env>`` is the name
of a tox environment. The operating system should be one of ``linux``,
``macosx``, or ``windows``. An example might be:

.. code:: yaml

    jobs:
    - template: run-tox-env.yml@OpenAstronomy
      parameters:
        envs:
        - linux: pep8
        - macosx: py37-test
        - windows: py36-docs

In many cases, this may be enough, but there are additional options you can
specify, which we describe in the following sections.

Reporting coverage
------------------

To enable coverage reporting, add a parameter ``coverage`` that is set to the
name of the service to use:

.. code:: yaml

    jobs:

    - template: run-tox-env.yml@OpenAstronomy
      parameters:
        coverage: codecov
        envs:
        - ...

At this time, only ``codecov`` is supported.

Non-Python dependencies
-----------------------

To make sure that non-Python dependencies are installed before the tox environments
are run, use the ``libraries`` parameter. This can have sections for the ``apt``,
``brew``, and ``choco`` tools which are used for ``linux``, ``macosx``, and ``windows``
respectively, and each of these sections should contain a list of package names to
install with these tools, e.g::

    jobs:

    - template: run-tox-env.yml@OpenAstronomy
      parameters:
        libraries:
          apt:
            - libopenjpeg5
          brew:
            - openjpeg
        envs:
        - ...

Note that as shown above, you don't need to specify all tools, only the ones for
which you need to install packages.

X virtual framebuffer
---------------------

If you want to make use of the X virtual framebuffer (Xvfb) which is typically needed
when testing packages that open graphical windows, you can set the ``xvfb`` parameter
to ``true``:

    jobs:

    - template: run-tox-env.yml@OpenAstronomy
      parameters:
        xvfb: true
        envs:
        - ...

This parameter only has an effect on Linux, and is ignored on other platforms.

Conda
-----

If you want tox to be run with `tox-conda
<https://github.com/tox-dev/tox-conda>`_, include the string ``conda`` in your
tox environment name. This will automatically result in conda getting set up,
and tox-conda installed.

Positional arguments for tox
----------------------------

If you want to make use of the ``{posargs}`` functionality in your ``tox.ini``
file, you can specify positional arguments to pass to tox for each job using the
``posargs`` parameter:

.. code:: yaml

    jobs:
    - template: run-tox-env.yml@OpenAstronomy
      parameters:
        envs:
        - linux: pep8
        - macosx: py37-test
          posargs: -n=4
        - windows: py36-docs

Setting or overriding options on a job by job basis
---------------------------------------------------

The ``coverage`` and ``libraries`` parameters can be specified on a job by job basis
instead of or as well as globally, and take precedence over global options:

.. code:: yaml

    jobs:
    - template: run-tox-env.yml@OpenAstronomy
      coverage: codecov
      libraries:
        brew:
        - fftw
      parameters:
        envs:
        - linux: pep8
          coverage: false
          libraries: {}
        - macosx: py37-test
        - windows: py36-docs
          libraries:
            choco:
              graphviz

In the above example, we have disabled coverage testing and any libaries for the
``pep8`` job, and overriden ``libraries`` so that ``graphviz`` gets installed on
Windows.

Python package release template
===============================

This template automates the process of building wheels as well as a source
distribution, and uploading them all to PyPI. Your project must be PEP-517 and
PEP-518 compatible in order to use this.

Configuring the PyPI service connection
---------------------------------------

If you plan to use this template to upload releases to PyPI, you will need to
first set up a PyPI service connection in Azure. To do this, go to the Azure
configuration for the repository where you want to use the templates. Then
click on **Project Settings** (in the bottom left as of 2019-09-18), then go
to the **Service connections** section in the settings.

Select **New Service Connection**, then **Python Package Upload**, and enter
the following information:

===================================== ========
**Connection Name:**                  a name for the connection, with no spaces, e.g. ``pypi_endpoint``

**Python repository url for upload:** this should be https://upload.pypi.org/legacy/ if you want to push the releases to the main PyPI server. Note that you can also use https://test.pypi.org/legacy/ if you want to test out the process using the Test PyPI server. Be sure to use https://, and include the '/' at the end of the URL since twine will otherwise fail.

**EndpointName**:                     for simplicity, you can set this to be the same as the connection name unless you have a good reason not to.

**Username**:                         this should be either your PyPI (or Test PyPI) username, or ``__token__`` if you want to use token authentication (note that in the latter case you should make sure the 'Username and Password' option is selected, **not** 'Authentication token'!).

**Password:**                         this should be either your PyPI (or Test PyPI) password, or the token if you want to use token authentication.
===================================== ========

If you want to use token authentication, you can create a token in your PyPI (or Test PyPI) settings.

Usage and options
-----------------

To make use of this template, add the following to the ``azure-pipelines.yml`` file:

.. code:: yaml

    jobs:
    - template: publish.yml@OpenAstronomy
      parameters:
        pypi_connection_name: 'pypi_endpoint'
        targets:
        - sdist
        - wheels_linux
        - wheels_macosx
        - wheels_windows

``pypi_connection_name`` should be set to the **Connection Name** you set above.
If the endpoint name you set is different from the connection name, you should
also specify the endpoint name with the ``pypi_endpoint_name`` parameter.
``targets`` should be set to a list of builds you want to generate - the four
options are shown in the example above (wheels for the three main platforms and
a source distribution) but you can choose to only build some of these if you
want. The initial ``if`` statement ensures that this process is only

If you want to run tests on the generated packages (which we recommend), you can make use of
the following parameters:

.. code:: yaml

    jobs:
    - template: publish.yml@OpenAstronomy
      parameters:
        pypi_connection_name: 'pypi_endpoint'
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
