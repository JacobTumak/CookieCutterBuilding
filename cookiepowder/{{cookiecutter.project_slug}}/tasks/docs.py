from invoke import task


@task
def clean(c):
    print("Cleaning...")
    c.run("rm -rf docs/build")  # replace with 'make clean'?


@task(clean)
def build(c):
    print("Building...")
    c.run("sphinx-build -b html docs/source docs/build/html")  # replace with 'make html'?
