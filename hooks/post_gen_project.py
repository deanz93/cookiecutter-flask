
from pathlib import Path
import shutil


TERMINATOR = "\x1b[0m"
WARNING = "\x1b[1;33m [WARNING]: "
INFO = "\x1b[1;33m [INFO]: "
HINT = "\x1b[3;33m"
SUCCESS = "\x1b[1;32m [SUCCESS]: "

DEBUG_VALUE = "debug"


def remove_open_source_files():
    """
    Removes open source files from the project.

    Removes the following files from the project:
        - CONTRIBUTORS.md
        - LICENSE

    These files are not needed for a closed source project.
    """
    file_names = ["CONTRIBUTORS.md", "LICENSE"]
    for file_name in file_names:
        Path(file_name).unlink()


def remove_gplv3_files():
    """
    Removes GPLv3 files from the project.

    Removes the following files from the project:
        - COPYING

    These files are only necessary for GPLv3 projects.
    """
    file_names = ["COPYING"]
    for file_name in file_names:
        Path(file_name).unlink()


def remove_utility_files():
    """
    Removes the utility directory from the project.

    This directory contains utility files such as scripts
    and other useful files.
    """
    try:
        shutil.rmtree("utility")
    except FileNotFoundError:
        pass


def remove_docker_files():
    """
    Removes the docker files from the project.

    Removes the following files from the project:
        - compose directory
        - docker-compose.local.yml
        - docker-compose.production.yml
        - .dockerignore

    These files are only necessary for projects with docker support.
    """
    shutil.rmtree("compose")

    file_names = [
        "docker-compose.local.yml",
        ".dockerignore",
        "Dockerfile",
        "entrypoint.sh",
    ]
    for file_name in file_names:
        Path(file_name).unlink()


def main():
    """
    Initializes the project.

    This function is called after the project has been generated.
    It removes any unnecessary files depending on the options
    chosen by the user.

    """
    if "{{ cookiecutter.open_source_license }}" == "Not open source":
        remove_open_source_files()

    if "{{ cookiecutter.open_source_license}}" != "GPLv3":
        remove_gplv3_files()

    if "{{ cookiecutter.use_docker }}".lower() == "y":
        remove_utility_files()
    else:
        remove_docker_files()

    print(SUCCESS + "Project initialized, keep up the good work!" + TERMINATOR)


if __name__ == "__main__":
    main()
