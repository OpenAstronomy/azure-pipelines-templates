
CI skip command check template
==============================

This template provides a job which parses the commit message of the pull
request, and if it contains a CI skip command such as ``[skip ci]`` it sets
a variable in the Azure Pipelines run. This variable can be used as a
condition on subsequent stages of the run, such that using a skip command
reduces the amount of building and testing.

For a CI skip command to be recognised for a job, the latest commit to the
pull request branch that triggered the Azure Pipelines run must have a
commit message that contains a recognised CI skip command in its first line.
Recognised commands include ``[skip ci]`` and ``[ci skip]``.
See :ref:`custom-skip-commands` for more details.

Basic setup
-----------

Firstly, ensure you load the templates under the ``OpenAstronomy``
namespace as described in :doc:`common`.
The following code shows how to place the job within a stage.

.. code:: yaml

    stages:
    - stage: StageOne
      jobs:
      - template: check-skip.yml@OpenAstronomy

The template must be called as a job within a stage prior to
the stages you want to conditionally skip.

Applying conditions to pipeline stages
--------------------------------------

The job provided by this template creates a variable in the Azure Pipelines run.
This variable is accessed at
``dependencies.STAGE_NAME.outputs['check_skip.search.found']``
where ``STAGE_NAME`` should be replaced with the name of the stage the template
was used within.

It will have a string value of either ``'true'`` or ``'false'``. It will be
``'true'`` if a skip command was found in the commit message and ``'false'``
otherwise.

This variable can be used to apply a condition to subsequent stages of the
run, for example,
``and(succeeded(), ne(dependencies.Setup.outputs['check_skip.search.found'], 'true'))``.

Example
-------

The following code provides an example of how to configure the stages
section of your ``azure-pipelines.yml`` file using this template.
Note that you will also need to make sure you first load the templates as
described in :doc:`common`.

.. code:: yaml

    stages:
    - stage: StageOneTests
      displayName: Basic Tests
      jobs:
      - template: check-skip.yml@OpenAstronomy
      - template: run-tox-env.yml@OpenAstronomy
        envs:
        - linux: py39

    - stage: StageTwoTests
      displayName: Detailed Tests
      condition: and(succeeded(), ne(dependencies.StageOneTests.outputs['check_skip.search.found'], 'true'))
      jobs:
      - template: run-tox-env.yml@OpenAstronomy
        envs:
        - macos: py39
        - windows: py39

In this example, the *Basic Tests* stage will always run, however, if a skip
command is in the commit message the *Detailed Tests* stage will not run.
As this template is independent of the other OpenAstronomy templates,
the stages conditions are applied to do not need to run jobs defined
using ``run-tox-env.yml``.

.. _custom-skip-commands:

Custom skip commands
--------------------

By default, the list of recognised skip commands are taken from the `Azure Pipelines documentation
<https://docs.microsoft.com/en-us/azure/devops/pipelines/scripts/git-commands?view=azure-devops&tabs=yaml#how-do-i-avoid-triggering-a-ci-build-when-the-script-pushes>`__.
This list includes ``[skip ci]`` and ``[ci skip]`` among others.

This default list can be replaced as shown in the following code.

.. code:: yaml

    stages:
    - stage: StageOne
      jobs:
      - template: check-skip.yml@OpenAstronomy
        commands: '"[skip ci]" "[ci skip]" noci'

This will configure the check to only recognise ``[skip ci]``, ``[ci skip]``
and ``noci`` as valid skip commands.
The value of ``commands`` must be a string of space separated skip commands,
with commands containing spaces inside double quotes.
Bash version 4.2 or above is required if specifying custom skip commands.
