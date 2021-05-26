import tests
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="Token Maker",
    version="0.0.1",
    description="Generate JWT token for Commonwell API use in DEV and QA environment",
    python_requires=">=3.6",
    packages=find_packages(exclude=['tests',]),
    include_package_data=True,
    zip_safe=True,
    install_requires=required,
    test_suite="tests",
    cmdclass={
        'test': tests.PyTest,
    }
)
