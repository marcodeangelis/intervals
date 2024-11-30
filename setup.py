from setuptools import find_packages, setup

setup(
    name='intervals',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    version='0.2.0',
    description='A modified version of the intervals library by Leslie',
    author='Marco, Leslie',
    license='MIT',
)