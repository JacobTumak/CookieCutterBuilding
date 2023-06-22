#!/usr/bin/env python
import os
import re
import sys
import subprocess
import datetime

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))

def replace_var_val(file_path, var_name, new_var_val):

    with open(file_path, "r") as file:
        content = file.read()

    # Construct the pattern to match the variable assignment
    pattern = r"{} = .*".format(re.escape(var_name))

    # Replace the variable assignment with the new value
    replaced_content = re.sub(pattern, "{} = '{}'".format(var_name, new_var_val), content)

    with open(file_path, "w") as file:
        file.write(replaced_content)

def get_py_ver():
    version_info = sys.version_info
    version_string = f"{version_info.major}.{version_info.minor}.{version_info.micro}"
    return version_string


if __name__ == '__main__':

    if '{{ cookiecutter.create_author_file }}' != 'y':
        remove_file('docs/AUTHORS.md')

    if 'no' in '{{ cookiecutter.command_line_interface|lower }}':
        cli_file = os.path.join('{{ cookiecutter.project_slug }}', 'cli.py')
        remove_file(cli_file)

    if 'Not open source' == '{{ cookiecutter.open_source_license }}':
        remove_file('LICENSE')


    filepath = "docs/sphinx/source/conf.py"
    var_name = "copyright"
    new_val = f'{datetime.datetime.now().year}, {{cookiecutter.copyright_entity}}'
    replace_var_val(filepath, var_name, new_val)

    # subprocess.run(['pip', 'install', '-r', 'requirements.txt'])
    # subprocess.run(['pip', 'install', '-r', 'requirements_dev.txt'])
