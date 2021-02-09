import json
import os
import subprocess

from setuptools import find_packages, setup

current_dir = os.path.dirname(__file__)


def get_version() -> str:
    return get_gitversion_output().get("SemVer", "0.0.1")


def get_gitversion_output() -> dict:
    cmd = os.path.normpath(
        os.path.join(current_dir, "..", ".tools", "GitVersion.CommandLine.5.3.7", "tools", "gitversion.exe")
    )
    out = subprocess.Popen([cmd, "/config", "..\\GitVersion.yml"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = out.communicate()
    utf8_out: str = stdout.decode(encoding="UTF-8")
    return json.loads(utf8_out)


def get_long_description() -> str:
    file_path = os.path.normpath(os.path.join(current_dir, "README.md"))
    with open(file_path, "r") as stream:
        return stream.read()


def get_requirements() -> list:
    file_path = os.path.normpath(os.path.join(current_dir + "/src", "requirements.txt"))
    requirements = []
    if os.path.isfile(file_path):
        with open(file_path, "r") as stream:
            requirements = stream.read().splitlines()
    return requirements


setup_args = {
    "name": "pipelayer",
    "version": "0.5.0",
    "description": "A lightweight pipeline framework",
    "long_description": get_long_description(),
    "long_description_content_type": "text/markdown",
    "url": "https://github.com/greater-than/PipeLayer",
    "classifiers": [
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    "author": "greaterThan, LLC",
    "author_email": "info@greaterthan.solutions",
    "packages": find_packages("src"),
    "package_dir": {"": "src"},
    "include_package_data": True,
    "install_requires": get_requirements(),
    "python_requires": ">=3.7"
}


setup(**setup_args)
