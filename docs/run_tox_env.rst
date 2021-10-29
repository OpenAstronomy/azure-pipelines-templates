
Tox template
============

The purpose of this template is to make it easy to map `tox
<https://tox.readthedocs.io/>`__ environments to Azure jobs. To use this
template, your repository will need to have a ``tox.ini`` file. Note that you
will also need to make sure you first load the templates as described in
:doc:`common`.

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
of a tox environment. The operating system should be one of ``linux``, ``linux32``,
``macos``, or ``windows``. An example might be:

.. code:: yaml

    jobs:
    - template: run-tox-env.yml@OpenAstronomy
      parameters:
        envs:
        - linux: pep8
        - macos: py37-test
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

To make sure that non-Python dependencies are installed before the tox
environments are run, use the ``libraries`` parameter. This can have sections
for the ``apt``, ``yum``, ``brew`` (or ``brew-cask``), and ``choco`` tools which
are used for ``linux``, ``linux32``, ``macos``, and ``windows`` respectively,
and each of these sections should contain a list of package names to install
with these tools, e.g:

.. code:: yaml

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

Pre-Tox Python dependencies
---------------------------

If you wish to install Python packages before tox is called, i.e. tox plugins,
you can pass the ``toxdeps`` parameter. These packages are installed at the same
time as tox itself.

.. code:: yaml

    jobs:

    - template: run-tox-env.yml@OpenAstronomy
      parameters:
        toxdeps: tox-pypi-filter
        envs:
        - ...

Commandline Arguments to tox
----------------------------

If you wish to pass extra command line arguments to the tox command, you can
specify ``toxargs``.

.. code:: yaml

    jobs:

    - template: run-tox-env.yml@OpenAstronomy
      parameters:
        envs:
        - linux: pep8
          toxargs: -i https://notpypi.org


X virtual framebuffer (Linux)
-----------------------------

If you want to make use of the X virtual framebuffer (Xvfb) which is typically needed
when testing packages that open graphical windows, you can set the ``xvfb`` parameter
to ``true``:

.. code:: yaml

    jobs:

    - template: run-tox-env.yml@OpenAstronomy
      parameters:
        xvfb: true
        envs:
        - ...

This parameter only has an effect on Linux, and is ignored on other platforms.

Mesa OpenGL (Windows)
---------------------

If you need to use OpenGL on Windows, you should set the ``mesaopengl`` option
to install the Mesa OpenGL libraries:

.. code:: yaml

    jobs:

    - template: run-tox-env.yml@OpenAstronomy
      parameters:
        mesaopengl: true
        envs:
        - ...

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
        - macos: py37-test
          posargs: -n=4
        - windows: py36-docs


Submodule Checkout
------------------

If you want to change the submodules setting to the `Checkout
<https://docs.microsoft.com/en-us/azure/devops/pipelines/yaml-schema?view=azure-devops&tabs=schema#checkout>`__
task you can set the ``submodules`` parameter. For instance:


.. code:: yaml

    jobs:
    - template: run-tox-env.yml@OpenAstronomy
      parameters:
        submodules: false
        envs:
        - linux: pep8


Setting or overriding options on a job by job basis
---------------------------------------------------

The ``coverage``, ``libraries``, ``posargs`` and ``xvfb`` parameters can be
specified on a job by job basis instead of or as well as globally, and take
precedence over global options:

.. code:: yaml

    jobs:
    - template: run-tox-env.yml@OpenAstronomy
      parameters:
        coverage: codecov
        posargs: '-n=4'
        libraries:
          brew:
          - fftw
        envs:
        - linux: pep8
          coverage: false
          libraries: {}
          posargs: ''
        - macos: py37-test
        - linux: py36-test
          xvfb: true
        - windows: py36-docs
          libraries:
            choco:
              graphviz

In the above example, we have disabled coverage testing, posargs, and any
libraries for the ``pep8`` job, and overridden ``libraries`` so that ``graphviz``
gets installed on Windows.

Naming Jobs
-----------

Optionally you can name an env, which is useful if you want to refer to that job
later in your pipeline, e.g. in the publish template's ``dependsOn`` parameter.

.. code:: yaml

    jobs:
    - template: run-tox-env.yml@OpenAstronomy
      parameters:
        envs:
        - linux: py36-test
          name: py36_test


Note, that job names in Azure pipelines can only contain `A-Z, a-z, 0-9, and
underscore
<https://docs.microsoft.com/en-us/azure/devops/pipelines/yaml-schema?view=azure-devops&tabs=schema#job>`__.
Which is why they are not automatically set from the tox env names, as they
frequently have hyphens in.

Caching
-------
Setting the ``cache_dirs`` parameter will cache all files in the specified
directories. If any of the files are updated or changed, the cache will be
automatically updated and re-uploaded at the end of a run.
The `Azure documentation
<https://docs.microsoft.com/en-us/azure/devops/pipelines/release/caching?view=azure-devops#using-the-cache-task>`__
contains more information on how Azure manages caching.

A list of caches are defined according to the following specification.

.. code:: yaml

    jobs:
    - template: run-tox-env.yml@OpenAstronomy
      parameters:
        cache_dirs:
        - <cache name>: <cached directory>
        - <cache name>: <cached directory>
      envs:
      - <os>: <tox env>
        cache_dirs:
        - <cache name>: <cached directory>
        - <cache name>: <cached directory>


All the files contained in the directory at the path specified by
``<cached directory>`` will be cached. This can be an absolute or relative
path, with relative paths based at ``$(System.DefaultWorkingDirectory)``,
which is usually the directory containing your package's ``setup.py`` file.
If this directory doesn't already exist, it will need to be created in your
testing code before writing files to it.

``<cache name>`` is the name of the cache.
Every cache is identified by a ``<cache name>`` and a ``<cached directory>``.
If either of these values are different, a new cache is created.
This name will also appear in the list of Azure tasks.

By defining ``cache_dirs`` under ``parameters``, the specified caches will be
used for all ``envs``. However, if ``cache_dirs`` is specified under a specific
environment, that environment will *only* use this set of caches.

In the following example three directories are cached, ``data_directory``, ``pref``
and ``out``. This examples has four unique caches, because it has four unique
pairs of cache names and directories.

The ``remote_data: data_directory``, ``preferences: pref`` and ``output: out``
caches are defined globally, so will be available in all ``envs`` except ``macos``
(i.e. ``linux`` and ``windows``) which has specified its own list of caches.
As ``macos`` defines its own list of caches, it *only* has access to the
``remote_data: data_directory`` and ``additional_preferences: pref`` caches.
Note that ``preferences: pref`` and ``additional_preferences: pref`` are
*different* caches, even though they are located at the same path.

.. code:: yaml

    jobs:
    - template: run-tox-env.yml@OpenAstronomy
      parameters:
        cache_dirs:
        - remote_data: data_directory
        - preferences: pref
        - output: out
      envs:
      - linux: py39
      - macos: py38-extra
        cache_dirs:
        - remote_data: data_directory
        - additional_preferences: pref
      - windows: py38


As an example, to cache pip packages you can set the ``PIP_CACHE_DIR`` environment variable
and cache this directory. This will ensure that ``pip`` uses this directory as the cache, and
that it is cached by Azure:

.. code:: yaml

    variables:
      PIP_CACHE_DIR: $(Pipeline.Workspace)/.pip

    jobs:
    - template: run-tox-env.yml@OpenAstronomy
      parameters:
        cache_dirs:
        - pip: $(PIP_CACHE_DIR)


Docker Jobs
-----------

This template has support for running tox inside docker containers. This was
originally added to support testing against 32bit linux builds using the
manylinux official docker images, so there is specific support for these images.
When using docker the Xvfb, conda and libraries options will not work.

Manylinux
#########

There are two options for using manylinux, you can set the os flag to either
``linux32`` or ``manylinux``. If it is set to ``linux32`` all the commands will
be prefixed with the ``linux32`` command to set the architecture to i686.

By setting the OS flag to ``manylinux`` or ``linux32``, the template will
automatically select docker and use the ``manylinux2010_i686`` image. Which can
be overridden by specifying the ``manylinux_image`` parameter.

When using ``manylinux`` images, the ``libraries`` parameter will work, and you
should use ``yum`` rather than ``apt`` as the tool name.

As a shortcut for the other docker options, when using ``manylinux`` you can set
``manylinux_image`` to the name of the container you want to use. This excludes
the ``quay.io/pypa`` prefix and also excludes any tag (``latest`` is always
used).

Other Docker Images
###################

You can also specify your own docker images in which to run tox. There are a few
options available to control this behaviour, they all can only be specified on a per-env basis.
The running of the docker commands are not dependant on the operating system,
although setting the os to ``linux32`` will cause all commands in the container
to be prefixed with the ``linux32`` setarch binary.
The following example shows all the possible options even though some are redundant:

.. code:: yaml

    jobs:
    - template: run-tox-env.yml@OpenAstronomy
      parameters:
        envs:
        - linux: <job name>
          docker_image: python:3.9.0rc1-slim-buster
          docker_name: python39
          docker_python: /usr/local/bin/python

The options are as follows:

* ``docker_image`` this is the name of the container to be created. It can be any valid argument to ``docker pull``, i.e ``python`` or ``quay.io/pypa/manylinux2010_i686``.
* ``docker_name`` this is optional as long as ``docker_image`` is a valid container name. If you specify a tag in ``docker_image`` ``:`` and ``/`` will be replaced, so you will not need to specify ``docker_name``. However, if you specify a more complex image you will need to manually specify the container name with ``docker_name``.
* ``docker_python`` this is the path inside the container to the docker executable.
