from setuptools import setup
from setuptools import find_packages

version = "0.1"

setup(name="generic",
      version=version,
      description="A set of tools for generic programming.",
      author="Andrey Popp",
      author_email="8mayday@gmail.com",
      license="BSD",
      packages=find_packages(exclude=["ez_setup", "examples", "tests"]),
      test_suite="generic.tests",
      zip_safe=True,
      )
