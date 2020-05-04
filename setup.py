from setuptools import setup, find_packages
from os import path
from io import open
from Cython.Build import cythonize


here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()
setup(
    name='sampleproject',
    install_requires="cython",
    version='1.3.1',
    description='A sample Python project',
    long_description=long_description,
    long_description_content_type='text/markdown',
    ext_modules = cythonize("test.pyx")
)
