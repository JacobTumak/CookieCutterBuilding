# This code is written in Python and contains a set of tasks that can be executed using the Invoke library.

# Import necessary libraries
from invoke import task
import re, os, toml, yaml, shutil

# Import configuration settings from tasks_conf.toml
with open("tasks/tasks_conf.toml", "r") as file:
    TASKS_CONF = toml.load(file)
PYPROJECT = TASKS_CONF['pyproject']
TEMPLATES = TASKS_CONF['file_templates']
SPHINX = TASKS_CONF['sphinx']
SPHINX_SOURCE = SPHINX['paths']['parent'] + SPHINX['paths']['source']

# Helper functions -----------
def item_in(item_name, location):
    """
    Checks if a package name is in a list of packages.
    Searches for items that start with the item name

    Args:
    package_name (str): The name of the package to check for.
    location (list): A list of packages to check.

    Returns:
    bool: True if the package name is in the list of packages, False otherwise.
    """
    return [package.startswith(item_name) for package in location][True]

def replace_var_val(file_path, var_name, new_var_val):
    """
    Replaces the value of a variable in a file.

    Args:
    file_path (str): The path to the file.
    var_name (str): The name of the variable to replace.
    new_var_val (str): The new value of the variable.

    Returns:
    None
    """
    with open(file_path, "r") as file:
        content = file.read()

    # Construct the pattern to match the variable assignment
    pattern = r"{} = .*".format(re.escape(var_name))

    # Replace the variable assignment with the new value
    replaced_content = re.sub(pattern, "{} = {}".format(var_name, new_var_val), content)

    with open(file_path, "w") as file:
        file.write(replaced_content)


def get_var_val(file_path, var_name):
    """
    Gets the value of a variable in a file.

    Args:
    file_path (str): The path to the file.
    var_name (str): The name of the variable to get the value of.

    Returns:
    str: The value of the variable.
    """
    with open(file_path, "r") as file:
        content = file.read()

    match = re.search(fr'{var_name}\s*=\s*["\'](.*?)["\']', content)
    if match:
        var_val = match.group(1)

    return var_val


def refactor_file(file_path, new_directory):
    """
    Moves a file to a new directory.

    Args:
    file_path (str): The path to the file.
    new_directory (str): The path to the new directory.

    Returns:
    None
    """
    # Get the file name from the file path
    file_name = file_path.split("/")[-1]

    # Construct the new file path in the new directory
    new_file_path = f"{new_directory}/{file_name}"

    # Move the file to the new directory
    shutil.move(file_path, new_file_path)

    print(f"File '{file_name}' has been refactored to '{new_file_path}'")
# End of helper functions ------------


@task
def start_sphinx(c):
    """
    Quick-start sphinx in docs/sphinx directory.

    Args:
    c: The context object.

    Returns:
    None
    """
    if not os.path.isdir('docs'):
        c.run('mkdir docs')
    c.run('mkdir docs/sphinx && cd docs/sphinx && sphinx-quickstart')


@task
def move_readme(c):
    """
    Moves the README file to the Sphinx source directory.

    Args:
    c: The context object.

    Returns:
    None
    """
    # compatible with .md and .rst
    for file in os.listdir():
        if file.startswith('README'):
            refactor_file(file, SPHINX['paths']['parent'])
            break


@task
def add_opt_deps(c):
    """
    Adds development dependencies to the pyproject.toml file.

    Args:
    c: The context object.

    Returns:
    None
    """
    opt_deps = PYPROJECT['optional_dependencies']

    # Open and parse the pyproject.toml file
    with open("pyproject.toml", "r") as file:
        toml_data = toml.load(file)

    # Add dependencies under [project.development-dependencies] section
    if "project" not in toml_data:
        toml_data["project"] = {}
    if "development-dependencies" not in toml_data["project"]:
        toml_data["project"]["optional-dependencies"] = {}
    for package in opt_deps:
        toml_data["project"]["optional-dependencies"][package] = opt_deps[package]

    # Write the updated content back to pyproject.toml
    with open("pyproject.toml", "w") as file:
        toml.dump(toml_data, file)


@task # TODO: figure out if this can be made version compliant?
def install_opt_deps(c):
    """
    Installs development dependencies using pip.

    Args:
    c: The context object.

    Returns:
    None
    """
    # Load the pyproject.toml file
    data = toml.load('pyproject.toml')

    # Get the development dependencies
    optional_dependencies = data.get('project', {}).get('optional-dependencies', {})

    # Install each development dependency using pip
    for packages in optional_dependencies.values():
        for package in packages:
            package = package.split(" ")[0]
            c.run(f"pip install {package}")


@task
def update_conf(c):
    """
    Updates the Sphinx configuration file.

    Args:
    c: The context object.

    Returns:
    None
    """
    file_path = SPHINX_SOURCE + "conf.py"
    exclude_pattern = SPHINX["conf"]["exclude_patterns"]
    if SPHINX["conf"]["html_theme"]:
        replace_var_val(SPHINX_SOURCE+"conf.py", "html_theme",SPHINX["conf"]["html_theme"])

    with open(file_path, "r") as file:
        lines = [line.rstrip() for line in file]

    updated_lines = [line.rstrip("]")+f" '{exclude_pattern}']"
                     if line.startswith("exclude_patterns")
                     else line for line in lines]

    with open(file_path, "w") as file:
        file.write("\n".join(updated_lines))


@task
def make_run_livereload(c):
    """
    Creates a run_livereload.py file.

    Args:
    c: The context object.

    Returns:
    None
    """
    if item_in("livereload", PYPROJECT['optional_dependencies']['docs']):
        filepath = SPHINX['paths']["parent"]+"run_livereload.py"
        with open(filepath, "w") as file:
            file.write(TEMPLATES['run_livereload'])
    else:
        print('"livereload" package not found in tasks_conf -> pyproject.dev_deps.docs')


@task
def update_index(c):
    """
    Updates the Sphinx index file.

    Args:
    c: The context object.

    Returns:
    None
    """
    filepath = SPHINX_SOURCE + 'conf.py'
    project_name = get_var_val(filepath, 'project')

@task
def make_rtd_conf(c):
    """
    This task generates the .readthedocs.yml file for ReadTheDocs configuration.

    Args:
    c: The invoke context.

    Returns:
    None
    """
    # Open the pyproject.toml file and load its contents into a dictionary
    with open("pyproject.toml", "r") as file:
        toml_data = toml.load(file)

    # Extract project information from pyproject.toml
    project_version = toml_data["project"]["version"]
    python_version = toml_data["project"]["requires-python"]

    rtd_config = TEMPLATES['rtd_config']
    rtd_config['version'] = project_version
    rtd_config['build']['tools']['python'] = python_version[2:]
    rtd_config['sphinx']['configuration'] = SPHINX_SOURCE + 'conf.py'


    # Generate the .readthedocs.yml file
    with open("docs/.readthedocs.yml", "w") as file:
        yaml.dump(rtd_config, file)

    print("Generated .readthedocs.yml file successfully.")