import nox
import pathlib


# https://www.youtube.com/watch?v=ImBvrDvK-1U&ab_channel=HynekSchlawack
# https://codewitholi.com/_posts/python-nox-automation/


nox.options.reuse_existing_virtualenvs = True
nox.options.sessions = [
    "sbom",
    "coverage",
    "lint",
    "tests_no_cov",
    # "release",
]


VERSIONS = [
    "3.9",
    "3.10",
    "3.11",
    "3.12",
]

ENV = {
    "GDRIVE_MOUNT": "tests/fixtures/GDRIVE",
    "LOCAL": "tests/fixtures/LOCAL",
    "LOCAL_EMPTY": "tests/fixtures/LOCAL_EMPTY",
}


@nox.session(python=VERSIONS, tags=["sbom"])
def sbom(session):
    """Runs Software Bill of Materials (SBOM)."""

    # print(session.bin)  # /home/michael/git/repos/pimo/.nox/dependencies-3-12/bin
    # print(session.bin_paths)  # ['/home/michael/git/repos/pimo/.nox/dependencies-3-12/bin']
    # print(session.cache_dir)  # .nox/.cache
    # # print(session.cd)
    # # print(session.chdir)
    # # print(session.conda_install)
    # # print(session.create_tmp)
    # # print(session.debug)
    # print(session.env)
    # # print(session.error)
    # # print(session.install)
    # # print(session.install_and_run_script)
    # print(session.interactive)  # True
    # print(session.invoked_from)  # /home/michael/git/repos/pimo
    # # print(session.log)
    # print(session.name)  # dependencies-3.12
    # # print(session.notify)
    # print(session.posargs)  # []
    # print(session.python)  # 3.12
    # # print(session.run)
    # # print(session.run_always)
    # # print(session.run_install)
    # # print(session.skip)
    # print(session.venv_backend)  # virtualenv
    # print(session.virtualenv.allowed_globals)  # ('uv',)
    # print(session.virtualenv.bin)  # /home/michael/git/repos/pimo/.nox/dependencies-3-12/bin
    # print(session.virtualenv.bin_paths)  # ['/home/michael/git/repos/pimo/.nox/dependencies-3-12/bin']
    # # print(session.virtualenv.create)
    # print(session.virtualenv.env)
    # print(session.virtualenv.interpreter)  # 3.12
    # print(session.virtualenv.is_sandboxed)  # True
    # print(session.virtualenv.location)  # /home/michael/git/repos/pimo/.nox/dependencies-3-12
    # print(session.virtualenv.location_name)  # .nox/dependencies-3-12
    # print(session.virtualenv.reuse_existing)  # True
    # print(session.virtualenv.venv_backend)  # virtualenv

    # https://pypi.org/project/pipdeptree/

    session.install(".[sbom]")

    # $ pipdeptree --graph-output dot > dependencies.dot
    # $ pipdeptree --graph-output pdf > dependencies.pdf
    # $ pipdeptree --graph-output png > dependencies.png
    # $ pipdeptree --graph-output svg > dependencies.svg
    # $ pipdeptree --mermaid > dependencies.svg

    # session.run("pipdeptree", "--json-tree", env=ENV)

    target_dir = pathlib.Path().cwd() / ".sbom"
    target_dir.mkdir(parents=True, exist_ok=True)

    # cyclonedx-py environment --output-format JSON --outfile {toxinidir}/.sbom
    session.run(
        "cyclonedx-py",
        "environment",
        "--output-format",
        "JSON",
        "--outfile",
        target_dir / f".cyclonedx-py.{session.name}.json",
        env=ENV,
    )
    # session.run("bash", "-c", f"pipdeptree --json-tree > .sbom_{session.name}.json", env=ENV)
    # session.run("pipdeptree", "--mermaid", ">", f".pipdeptree.{session.name}.mermaid", env=ENV, external=True)
    session.run(
        "bash",
        "-c",
        f"pipdeptree --mermaid > {target_dir}/.pipdeptree.{session.name}.mermaid",
        env=ENV,
        external=True,
    )
    # session.run(
    #     "bash",
    #     "-c",
    #     f"pipdeptree --graph-output png > {target_dir}/.pipdeptree.{session.name}.png",
    #     env=ENV,
    #     external=True,
    # )
    # # session.run("coverage", "report")  # report to console
    # # session.run("coverage", "xml")  # ./coverage.xml
    # # session.run("coverage", "html")  # ./htmlcov/


@nox.session(python=VERSIONS, tags=["coverage"])
def coverage(session):
    """Runs coverage"""

    session.install(".[coverage]")

    session.run(
        "coverage", "run", "--source", "src", "-m", "pytest", "-sv", env=ENV
    )  # ./.coverage
    session.run("coverage", "report")  # report to console
    # session.run("coverage", "xml")  # ./coverage.xml
    # session.run("coverage", "html")  # ./htmlcov/


@nox.session(python=VERSIONS, tags=["lint"])
def lint(session):
    """Runs linters and fixers"""
    # session.run("poetry", "install", external=True)

    session.install(".[lint]")

    session.run("black", "src")
    session.run("isort", "--profile", "black", "src")

    # # nox > Command pylint src failed with exit code 30
    # # nox > Session lint-3.12 failed.
    # session.run("pylint", "src")
    # # https://github.com/actions/starter-workflows/issues/2303#issuecomment-1973743119
    session.run("pylint", "--exit-zero", "src")
    # session.run("pylint", "--disable=C0114,C0115,C0116", "--exit-zero", "src")
    # https://stackoverflow.com/questions/7877522/how-do-i-disable-missing-docstring-warnings-at-a-file-level-in-pylint
    # C0114 (missing-module-docstring)
    # C0115 (missing-class-docstring)
    # C0116 (missing-function-docstring)


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
