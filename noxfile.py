import os
import nox


# https://www.youtube.com/watch?v=ImBvrDvK-1U&ab_channel=HynekSchlawack
# https://codewitholi.com/_posts/python-nox-automation/


nox.options.reuse_existing_virtualenvs = True
# nox.options.sessions = ["lint", "tests"]


VERSIONS = ["3.9", "3.10", "3.11", "3.12", "3.13"]

ENV = {
    "GDRIVE_MOUNT": "tests/fixtures/GDRIVE",
    "LOCAL": "tests/fixtures/LOCAL",
    "LOCAL_EMPTY": "tests/fixtures/LOCAL_EMPTY",
}


@nox.session(python=VERSIONS, tags=["coverage"])
def coverage(session):
    """ Runs coverage """

    session.install(".[coverage]")

    session.run("coverage", "run", "--source", "src", "-m", "pytest", "-sv", env=ENV)  # ./.coverage
    session.run("coverage", "report")  # report to console
    # session.run("coverage", "xml")  # ./coverage.xml
    # session.run("coverage", "html")  # ./htmlcov/


@nox.session(python=VERSIONS, tags=["lint"])
def lint(session):
    """ Runs linters and fixers """
    # session.run("poetry", "install", external=True)

    session.install(".[lint]")

    session.run("black", "src")
    session.run("isort", "--profile", "black", "src")
    session.run("pylint", "src")


@nox.session(python=VERSIONS, tags=["tests"])
def tests_no_cov(session):
    session.install(".[tests]")

    session.run(
        "pytest",
        *session.posargs,
        env=ENV,
    )


@nox.session(python=VERSIONS, tags=["release"])
def release(session):
    """Build and release to a repository"""
    session.install(".[release]")

    session.skip("Not implemented")

    raise NotImplementedError

    # pypi_user: str = os.environ.get("PYPI_USER")
    # pypi_pass: str = os.environ.get("PYPI_PASS")
    # if not pypi_user or not pypi_pass:
    #     session.error(
    #         "Environment variables for release: PYPI_USER, PYPI_PASS are missing!",
    #     )
    # session.run("poetry", "install", external=True)
    # session.run("poetry", "build", external=True)
    # session.run(
    #     "poetry",
    #     "publish",
    #     "-r",
    #     "testpypi",
    #     "-u",
    #     pypi_user,
    #     "-p",
    #     pypi_pass,
    #     external=True,
    # )
