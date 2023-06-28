import subprocess
import re
from django.core.management.utils import get_random_secret_key

subprocess.run(['pip', 'install', '-q', 'django'])
django_secret = get_random_secret_key()

with open('{{cookiecutter.project_slug}}/settings.py', "r") as file:
    content = file.read()

# Construct the pattern to match the variable assignment
pattern = r"{} = .*".format(re.escape('SECRET_KEY'))

# Replace the variable assignment with the new value
replaced_content = re.sub(pattern, "{} = '{}'".format('SECRET_KEY', django_secret), content)

with open('{{cookiecutter.project_slug}}/settings.py', "w") as file:
    file.write(replaced_content)