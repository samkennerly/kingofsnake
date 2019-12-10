#!/usr/bin/env python

from setuptools import find_packages, setup


def read(path):
    with open(path) as f:
        return "".join(f)


kw = {
    "author": "Sam Kennerly",
    "author_email": "samkennerly@gmail.com",
    "classifiers": [
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
    ],
    "description": "Template for a containerized Python project.",
    "install_requires": ["pytest"],
    "keywords": "development docker environment kitchen sandbox template testing",
    "license": read("LICENSE"),
    "long_description": read("README.md"),
    "long_description_content_type": "text/markdown",
    "name": "pydiner",
    "package_data": {"": ["*.md"]},
    "package_dir": {"": "src"},
    "packages": find_packages(where="src"),
    "python_requires": ">=3.7.5, <4",
    "url": "https://github.com/samkennerly/pydiner/",
    "version": "0.2.0",
}

if __name__ == "__main__":
    setup(**kw)
