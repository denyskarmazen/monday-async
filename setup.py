from setuptools import setup


def read_version_info():
    version_info = {}
    with open("monday_async/_version.py") as file:
        exec(file.read(), version_info)
    return version_info


version = read_version_info()


with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="monday-async",
    author="JUSTFUN0368",
    author_email="deniskarmazen@gmail.com",
    version=version["__version__"],
    description='An asynchronous Python client library for monday.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=requirements,
    python_requires=">=3.10"
)
