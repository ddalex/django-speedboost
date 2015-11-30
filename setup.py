#!/usr/bin/env python
# coding: utf-8

import os
import shutil
import importlib

from distutils.core import setup, Extension
from Cython.Compiler.Main import compile


class CythonModuleCompiler(list):
    def __init__(self):
        self.module_list = ['django.template.base', 'django.template.context']
        self._cache = {}

    def _mangle_module(self, module_name):
        if module_name in self._cache:
            return self._cache[module_name]

        source_file_name = importlib.import_module(module_name).__file__
        if source_file_name.endswith(".pyc"):
            source_file_name = source_file_name[:-1]
        base_name = os.path.basename(source_file_name)

        # generate the C files if they are not there
        if not os.path.exists(os.path.join("django_cemplate", base_name.replace(".py", ".c"))):
            shutil.copy2(source_file_name, "django_cemplate")
            c_file_name = compile(os.path.join("django_cemplate", base_name)).c_file
            os.remove(os.path.join("django_cemplate", base_name))
        else:
            c_file_name = os.path.join("django_cemplate", base_name.replace(".py", ".c"))

        print "C_file_name", c_file_name
        self._cache[module_name] = Extension("django_cemplate.{0}".format(base_name[:-3]), sources=[c_file_name], package="django_cemplate")
        return self._cache[module_name]

    def __getitem__(self, key):
        module = self.module_list[key]
        return self._mangle_module(module)

    def __iter__(self):
        for module in self.module_list:
            yield self._mangle_module(module)

    def __len__(self):
        l = len(self.module_list)
        return l

setup(
    name="django-django_cemplate",
    author="Alex DAMIAN",
    author_email="ddalex@gmail.com",
    version="0.1",
    license="GPL",
    url="https://github.com/ddalex/django-django_cemplate",
    download_url="https://github.com/ddalex/django-django_cemplate/releases",
    description="Cython-compiles django.template.[base,context,context_processors].py files for speed improvements.",
    packages=["django_cemplate"],
    ext_modules=CythonModuleCompiler(),
    install_requires=['django', 'cython'],
    scripts=""
)
