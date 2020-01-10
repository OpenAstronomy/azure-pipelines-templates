Setting up Azure Pipelines for a GitHub repository
==================================================

If you already know how to set up Azure Pipelines for a repository and just
want to find out about how to use the templates, you can jump ahead to
:doc:`common`.

Before we start setting up Azure Pipelines, we need to make sure that an
``azure-pipelines.yml`` file exists somewhere in the main (upstream) repository
you are setting up. This can be problematic in that you may not want to add a
configuration file to your ``master`` branch until you know it works properly.
Instead, you will likely want to create the configuration file in a branch of
your fork, and then iterate on it in a pull request to your main repository.

To get around this, the easiest way is to first make a temporary branch in your
main repository called e.g. ``tmp-azure`` (we will use that name for this
guide), and adding a file called ``azure-pipelines.yml`` that contains just a
single ``#`` character (completely empty files are ignored by Azure). Once you
have done this, you can proceed with setting up Azure Pipelines:

#. If you haven't already done so, make sure you create a (free) account
   at http://dev.azure.com/. If needed, you can also create an organization
   (if possible, try and use the same name as the user/organization on GitHub).

#. Click on **New Project** to set up Azure Pipelines for a repository. Use the
   repository name for the project name, and choose to make the project public.
   Click on **Create**.

#. You will now be asked where your code lives (if this doesn't happen, go to
   the **Pipelines** section and click on **Create Pipeline**). Select **GitHub**.

#. You will then be asked to select your repository. If you don't see it in the
   list, enter its name in the filter box. If you still don't see it, change
   **My repositories** to **All repositories**. Click on your repository. At this
   point, you may be taken to GitHub to approve Azure being set up for your
   repository. Scroll down on the GitHub page and click on **Approve and install**.
   You will now be redirected back to Azure Pipelines.

#. At this point, Azure will ask you to review your pipeline YAML. It may have found
   the quasi-empty file we created before, but if not, you can point it to the
   ``tmp-azure`` branch and select the ``azure-pipelines.yml`` file. Once you see
   the empty file with the single ``#``, you are ready to go, so click **Run**.

Since the configuration is empty, you will get an error about parsing the configuration
file, but you can just ignore this. You are now ready to open a pull request to your
repository adding a real ``azure-pipelines.yml`` file, and you can also now remove
the ``tmp-branch`` from your repository.
