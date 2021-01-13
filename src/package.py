import os
import shlex
import subprocess
from distutils.dist import Distribution
from typing import Any

from setuptools import Command

WHEELHOUSE = ".wheelhouse"


class Package(Command):
    """
    Package code and dependencies into wheelhouse
    """

    def __init__(self, dist: Distribution) -> None:
        super().__init__(dist)

    def initialize_options(self) -> None:
        pass

    def finalize_options(self) -> None:
        pass

    def localize_requirements(self) -> None:
        """
        After the package is unpacked at the target destination, the requirements can be installed
        locally from the wheelhouse folder using the option --no-index on pip install which
        ignores the package index (onlly looking at --find-lins URLs instead).

        --find-links <url | path> looks for archive from url or path.

        Since the original requirements.txt might have links to a non pip repo such as github (https),
        it will parse the links for the archive from a url an not from teh wheelhouse.
        This function creates a new requirements.txt with the only name and version for each of
        the packages, thus eliminating the need to fetch/parse links from http sources and install
        all archives from the wheelhouse
        """
        dependencies = open("requirements.txt").read().split("\n")
        local_dependencies = []

        for dependency in dependencies:
            if dependency:
                if "egg=" in dependency:
                    pkg_name = dependency.split("egg=")[-1]
                    local_dependencies.append(pkg_name)
                elif "git+" in dependency:
                    pkg_name = dependency.split("/")[-1].split(".")[0]
                else:
                    local_dependencies.append(dependency)

        print(f"Local packages in wheel: {local_dependencies}")
        self.execute("mv requirements.txt requirements.orig")

        with open("requirements.txt", "w") as requirements_file:
            # Filter is used to remove empy list members
            requirements_file.write("\n".join(filter(None, local_dependencies)))

    def execute(self, command: str, capture_output: bool = False) -> Any:
        """
        The excute command will loop and keep reading the stdout, check for
        the return code, and display the output in real time.
        """

        print(f"Running shell command: {command}")

        if capture_output:
            return subprocess.check_output(shlex.split(command))

        process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)

        while True:
            std_out = process.stdout
            output: bytes = bytes()
            if isinstance(std_out, bytes):
                output = process.stdout.readline()

            if not output.__len__ and process.poll() is not None:
                break
            if output:
                print(output.strip())

        return_code = process.poll()

        if return_code != 0:
            print(f"Error running command '{command} - exit code {return_code}'")
            raise IOError("Shell Command Failed")

        return return_code

    def run_commands(self, commands: list) -> None:
        for command in commands:
            self.execute(command)

    def restore_requirements_txt(self) -> None:
        if os.path.exists("requirements.orig"):
            commands = [
                "rm requirments.txt",
                "mv requirments.orig requirements.txt"
            ]
            self.run_commands(commands)

    def run(self) -> None:
        commands = [
            f"rm -rf {WHEELHOUSE}",
            f"mkdir -p {WHEELHOUSE}",
            f"pip wheel --wheel-dir{WHEELHOUSE} -r requirements.txt"
        ]
        print("Packaging requirements.txt into wheelhouse")
        self.run_commands(commands)

        print("Generating local requirements.txt")
        self.localize_requirements()

        print("Packaging code and wheelhouse into dist")
        self.run_commands(["sdist"])

        print("Restoring original requirements.txt file")
        self.restore_requirements_txt()
