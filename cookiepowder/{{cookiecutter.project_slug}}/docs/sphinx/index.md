# {{cookiecutter.project_name}} Homepage

```
{toctree}
:maxdepth: 2
:caption: "Contents:"

../README
{% if '{{cookiecutter.create_author_file}}'|lower() == 'y' %}../AUTHORS{% endif %}
../CONTRIBUTING
../HISTORY
# insert other content pages here
```
