#!/usr/bin/env python
# coding: utf-8

import os
import sys

from distutils.core import setup
from distutils.extension import Extension

from distutils import sysconfig

site_packages_path = sysconfig.get_python_lib(plat_specific=True)
site_packages_rel_path = site_packages_path[len(sysconfig.EXEC_PREFIX) + 1:]

USE_CYTHON = False
if 'cython' in sys.argv:
    sys.argv.remove('cython')
    USE_CYTHON = True

extensions = []
for d, s, files in os.walk("django_speedboost"):

    for fname in files:
        if fname.endswith(".c"):
            basename = fname[:-2]
            extensions.append(Extension(os.path.join(d, basename), [os.path.join(d, fname)]))

if USE_CYTHON:
    from Cython.Build import cythonize
    from Cython.Compiler.Options import directive_defaults

    directive_defaults['linetrace'] = True
    directive_defaults['binding'] = True
    extensions = cythonize("django_speedboost/*.py*")

setup(
    name="django_speedboost",
    author="Alex DAMIAN",
    author_email="ddalex@gmail.com",
    version="1.00.rc3",
    license="GPL",
    url="https://github.com/ddalex/django-cemplate",
    download_url="https://github.com/ddalex/django-cemplate/releases",
    description="Cython-compiles django.template.[base,context,context_processors].py files for speed improvements.",
    packages=["django_speedboost"],
    ext_modules=extensions,
    install_requires=['django==1.8.7'],
    data_files=[(site_packages_rel_path, ["django_speedboost.pth"])],
    scripts="",
)
