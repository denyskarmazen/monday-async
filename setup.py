from setuptools import setup


def read_version_info():
    version_info = {}
    with open("monday_async/_version.py") as file:
        exec(file.read(), version_info)
    return version_info


version = read_version_info()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="monday_async",
    version=version["__version__"],
    description='An asynchronous Python client library for monday.com',
    install_requires=requirements
)
