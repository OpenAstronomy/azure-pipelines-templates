******************************
SunPy Azure Pipeline Templates
******************************

This a template that will help simplify the `Azure Pipelines <https://azure.microsoft.com/en-gb/services/devops/pipelines/>`__ configuration when using `tox <https://tox.readthedocs.org>`__ to drive your CI.

Borrowed heavily from `tox's templates <https://github.com/tox-dev/azure-pipelines-template>`__.

Usage
=====

**First configure a github service connection**:

It is suggested to use a generic name, such as ``sunpyorg`` so forks can also configure the same.

You can find this in ``Project Settings => Service connections`` in the Azure Devops dashboard for your project.
Project settings is located in the bottom left corner of the UI as of 2019-04-30.
Below I'm using the endpoint name ``sunpyorg``.

**To load the template, add this to the beginning of the ``azure-pipelines.yml``**

.. code:: yaml

    resources:
      repositories:
      - repository: sunpy
        type: github
        endpoint: sunpyorg
        name: sunpy/azure-pipelines-template
        ref: master


This will make the templates in this repository available in the ``sunpy`` namespace.
Note the ref allows you to pin the template version you want, you can use ``refs/master`` if you want latest version.

job templates
-------------

run-tox-env.yml
^^^^^^^^^^^^^^^

You must have a ``tox.ini`` and a ``azure-pipelines.yml`` file in your main repository.
Then for each job you want to run, you have to create a entry for it within your ``azure-pipelines.yml`` file.

Example
"""""""

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

* ``name`` : Name of the build
* ``os``: The operating system to use - ``windows``, ``macos``, ``linux``
* ``tox`` : The name of the tox environment as well as any extra inputs to pytest.

publish-pypi.yml
^^^^^^^^^^^^^^^^

This job template will publish the Python package in the current folder (both ``sdist`` and ``wheels``) via the PEP-517/8 build mechanism and twine.

Your project must be PEP-517 and PEP-518 compatible.
A PyPi remote is configured via Azure Pipelines project dashboard.

Example
"""""""

.. code:: yaml

    - ${{ if startsWith(variables['Build.SourceBranch'], 'refs/tags/') }}:
      - template: publish-pypi.yml@sunpy
        parameters:
          pypi_remote: 'pypi_sunpy'
          dependsOn: [Linux_37_offline]

The parameters are:

* ``pypi_remote`` - The pypi remote to upload to.
* ``dependsOn`` - Jobs this job depends on.
