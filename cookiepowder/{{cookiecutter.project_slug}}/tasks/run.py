import sphinx_rtd
from invoke import task

ORIG_FILE = """
from invoke import Collection

import run

ns = Collection(run)"""


# Define tasks using invoke package
@task(sphinx_rtd.add_opt_deps,
      sphinx_rtd.install_opt_deps,
      sphinx_rtd.start_sphinx)
def init_sphinx(c):
    """
    This task initializes Sphinx by running the add_dev_deps, install_dev_deps, and start_sphinx tasks.
    """
    print('Initializing Sphinx')

@task(sphinx_rtd.update_index,
      sphinx_rtd.update_conf,
      sphinx_rtd.make_run_livereload)
def setup_sphinx(c):
    """
    This task sets up Sphinx by running the update_index, update_conf, and create_run_livereload tasks.
    """
    print("Setting up Sphinx")


with open('tasks/__init__.py','r') as file:
    contents = [line.split(" ") for line in file if line.startswith('import')][0]


if "pypi_pub," not in contents:

    @task
    def show_all(c):
        with open('tasks/__init__.py', 'r') as file:
            lines = [line.rstrip() for line in file]

        updated_lines = []
        for line in lines:
            if line.startswith("import"):
                updated_lines.append(line + f", {'pypi_pub'}" + f", {'sphinx_rtd'}")
            if line.startswith('ns'):
                updated_lines.append(line.rstrip(')') + f", {'pypi_pub'}" + f", {'sphinx_rtd'})")
            else:
                updated_lines.append(line)

        with open('tasks/__init__.py', "w") as file:
            file.write("\n".join(updated_lines))
else:
    @task
    def hide_extra(c):
        with open('tasks/__init__.py', 'w') as file:
            if len(ORIG_FILE) > 1:
                file.write(ORIG_FILE)
            else:
                print("run.ORIG_FILE is empty and can't overwrite current tasks/__init.py")
