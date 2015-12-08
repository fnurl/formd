"""Setup file for formd using setuptools.

Contributed by @fnurl
"""
from setuptools import setup

setup(
    name='formd',
    version='1.0.0',
    description='A Markdown formatting tool',
    author='Seth Brown',
    author_email='sethbrown@drbunsen.org',
    url='http://drbunsen.github.com/formd/',
    packages=['formd', ],
    entry_points={
        'console_scripts': ['formd=formd.command_line:main'],
    },
    requires=['markdown (>=2.0)', ],
    license='MIT',
    long_description=open('README.md').read(),
)
