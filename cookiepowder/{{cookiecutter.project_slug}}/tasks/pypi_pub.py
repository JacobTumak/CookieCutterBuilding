from invoke import task
import toml, yaml

with open('tasks/tasks_conf.toml', 'r') as file:
    TASKS_CONF = toml.load(file)


@task
def add_build_reqs(c):
    build_reqs = TASKS_CONF['pyproject']['build']['requires']

    with open('pyproject.toml', 'r') as file:
        toml_data = toml.load(file)
    try:
        for package_name in build_reqs:
            if package_name not in toml_data['build-system']['requires']:
                toml_data['build-system']['requires'].append(package_name)
    except:
        toml_data['build-system']['requires'] = build_reqs

    with open('pyproject.toml', 'w') as file:
        toml.dump(toml_data, file)


@task
def install_build_reqs(c):
    with open('pyproject.toml','r') as file:
        toml_data = toml.load(file)
    for package in toml_data['build-system']['requires']:
        c.run(f'pip install {package}')


@task
def upgrade_twine(c):
    c.run('pip install --upgrade twine')


# TODO: Check if "dist" is correct
@task
def test_twine_upload(c):
    c.run('twine upload --repository testpypi dist/*')


@task(upgrade_twine)
def twine_upload(c):
    c.run('twine upload --repository pypi dist/*')