from setuptools import setup, find_packages
from setuptools_scm import get_version


setup(
    name="ert-client",
    author="Equinor ASA",
    description="ERT API client library",
    url="https://github.com/Equinor/ert-client",
    packages=find_packages(exclude=["tests"]),
    license="GPL-3.0",
    platforms="any",
    install_requires=["numpy", "pandas", "requests"],
    version=get_version(relative_to=__file__, write_to="ertapi/__version__.py"),
)
