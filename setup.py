from setuptools import setup, find_packages

setup(
    name="research_digest",
    version="0.1.0",
    author="Aryan Dhawan",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)