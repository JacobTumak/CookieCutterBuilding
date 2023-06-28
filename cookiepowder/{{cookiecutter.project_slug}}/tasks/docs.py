from invoke import task
import toml


@task
def install_deps(c):
    # Load pyproject.toml file
    with open("pyproject.toml", "r") as f:
        pyproject = toml.load(f)

    # Install core dependencies
    if "dependencies" in pyproject["project"]:
        for dep in pyproject["project"]["dependencies"]:
            c.run(f"pip install {dep}")

    # Install optional dependencies
    if "optional-dependencies" in pyproject["project"]:
        for opt_dep_list in pyproject["project"]["optional-dependencies"].values():
            for opt_dep in opt_dep_list:
                c.run(f"pip install {opt_dep}")

    print("Dependencies installed successfully.")


@task
def clean(c):
    print("Cleaning...")
    c.run("rm -rf docs/build")  # replace with 'make clean'?


@task(clean)
def build(c):
    print("Building...")
    c.run("sphinx-build -b html docs/source docs/build/html")  # replace with 'make html'?
