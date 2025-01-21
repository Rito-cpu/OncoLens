from setuptools import find_packages, setup
from package import Package


setup(
    name="IMO-modeling",
    version="1.0.0",
    author="Paul Llamas",
    author_email="paul.llamas99@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    cmdclass={
        "package": Package
    }
)
