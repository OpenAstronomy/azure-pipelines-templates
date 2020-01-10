======================================
OpenAstronomy Azure Pipeline Templates
======================================

This repository contains set of templates for `Azure Pipelines
<https://azure.microsoft.com/en-gb/services/devops/pipelines/>`_ that helps
simplify configuration in individual packages. At this time, there are two main
templates available - one to make it easy to map `tox
<https://tox.readthedocs.org>`__ environments to builds on Azure Pipelines, and
one to automate the process of releasing Python packages.

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   setup
   common
   run_tox_env
   publish

The templates in this repository were inspired and adapted from `tox's
<https://github.com/tox-dev/azure-pipelines-template>`__ and `SunPy's templates
<https://github.com/sunpy/azure-pipelines-template>`_.
