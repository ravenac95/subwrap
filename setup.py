from setuptools import setup, find_packages
import sys, os

VERSION = '0.0.1'

LONG_DESCRIPTION = open('README.rst').read()

setup(name='subwrap',
    version=VERSION,
    description="subwrap - A simple wrapper for subprocess",
    long_description=LONG_DESCRIPTION,
    author='Reuven V. Gonzales',
    author_email='reuven@tobetter.us',
    url="https://github.com/ravenac95/subwrap",
    license='MIT',
    platforms='Unix',
    py_modules=['subwrap'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    entry_points={},
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Operating System :: POSIX',
        'Programming Language :: Python',
    ],
)
