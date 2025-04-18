from setuptools import setup, find_packages

setup(
    name="movies-collector",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'pandas~=2.2.3',
        'requests~=2.31.0'
    ],
)