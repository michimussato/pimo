import nox
import logging


_logger = logging.getLogger(__name__)

# https://www.youtube.com/watch?v=ImBvrDvK-1U&ab_channel=HynekSchlawack
# https://codewitholi.com/_posts/python-nox-automation/


VERSIONS = ["3.9", "3.10", "3.11", "3.12", "3.13"]

ENV = {
    "GDRIVE_MOUNT": "tests/fixtures/GDRIVE",
    "LOCAL": "tests/fixtures/LOCAL",
    "LOCAL_EMPTY": "tests/fixtures/LOCAL_EMPTY",
}


@nox.session(python=VERSIONS, tags=["tests"])
def tests_no_cov(session):
    session.install(".[tests]")

    session.run(
        "pytest",
        *session.posargs,
        env=ENV,
    )


@nox.session(python=VERSIONS, tags=["lint"])
def lint(session):
    """ Runs linters and fixers """
    # session.run("poetry", "install", external=True)

    session.install(".[lint]")

    session.run("black", "src")
    session.run("isort", "--profile", "black", "src")
    session.run("pylint", "src")


@nox.session(python=VERSIONS, tags=["tests"])
def tests_no_cov_after_lint(session):
    session.install(".[tests]")

    session.run(
        "pytest",
        *session.posargs,
        env=ENV,
    )
