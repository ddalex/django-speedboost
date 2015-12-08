#!/usr/bin/env python
# coding: utf-8

from distutils.core import setup
from Cython.Build import cythonize

from Cython.Compiler.Options import directive_defaults

from distutils import sysconfig
site_packages_path = sysconfig.get_python_lib()

directive_defaults['linetrace'] = True
directive_defaults['binding'] = True

setup(
    name="django_cemplate",
    author="Alex DAMIAN",
    author_email="ddalex@gmail.com",
    version="0.99",
    license="GPL",
    url="https://github.com/ddalex/django-cemplate",
    download_url="https://github.com/ddalex/django-cemplate/releases",
    description="Cython-compiles django.template.[base,context,context_processors].py files for speed improvements.",
    packages=["django_cemplate"],
    ext_modules=cythonize("django_cemplate/*.py*"),
    install_requires=['django==1.8.7', 'cython'],
    data_files=[(site_packages_path, ["django_cemplate.pth"])],
    scripts="",
)
