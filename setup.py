from setuptools import setup
from setuptools import find_packages

version = "0.3"
long_description = \
        open("README.rst", "r").read() + \
        "\n\n" + \
        open("CHANGELOG.rst", "r").read()

setup(name="generic",
      version=version,
      description="A set of tools for generic programming.",
      long_description=long_description,
      author="Andrey Popp",
      author_email="8mayday@gmail.com",
      license="BSD",
      packages=find_packages(exclude=["ez_setup", "examples", "tests"]),
      test_suite="generic.tests",
      zip_safe=True,
      )
