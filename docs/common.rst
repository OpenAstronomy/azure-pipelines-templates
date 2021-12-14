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

where ``<service connection name>`` is the name of the service connection you
set up above. This will make the templates in this repository available in the
``OpenAstronomy`` namespace in the rest of the file.

.. note::
   Specifying the ``ref`` property for the ``OpenAstronomy`` repository is not
   recommended because the default branch of the ``azure-pipelines-templates``
   repository may change in the future.
   `Azure Pipelines will use the current default branch when a ref is not specified.
   <https://docs.microsoft.com/en-us/azure/devops/pipelines/repos/multi-repo-checkout?view=azure-devops#checking-out-a-specific-ref>`__
