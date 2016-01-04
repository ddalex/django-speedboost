# -*- encoding:utf-8 -*-
from __future__ import absolute_import, division, unicode_literals, print_function

import importlib
import sys

MODULE_NAMES = ["context", "context_processors", "base", "defaulttags"]


for module_name in MODULE_NAMES:
    assert "django.template.%s" % module_name not in sys.modules


class DjangoCemplateImporter():

    original_template_modules = ["django.template.%s" % module_name for module_name in MODULE_NAMES]
    replcmnt_template_modules = ["django_speedboost.%s" % module_name for module_name in MODULE_NAMES]
    paths = {}

    def find_module(self, full_name, path=None):
        if full_name in self.original_template_modules:
            self.paths[full_name] = path
            return self
        if full_name.startswith("django_speedboost.") and full_name not in self.replcmnt_template_modules:

            sys.meta_path.remove(_instance)
            try:
                importlib.import_module(full_name.replace("django_speedboost.", "django.template."))
            except ImportError:
                return None
            finally:
                sys.meta_path.append(_instance)

            return self
        return None

    def load_module(self, name):
        if name in sys.modules:
            return sys.modules[name]
        if name in self.original_template_modules:
            global _instance
            imported_module = importlib.import_module(name.replace("django.template", "django_speedboost"))
            sys.modules[name] = imported_module
            return imported_module
        elif name.startswith("django_speedboost.") and name not in self.replcmnt_template_modules:
            m_name = name.replace("django_speedboost", "django.template")
            global _instance
            sys.meta_path.remove(_instance)
            imported_module = importlib.import_module(m_name)
            sys.meta_path.append(_instance)
            sys.modules[name] = imported_module
            return imported_module

        raise ImportError("Could not load %s" % name)


_instance = None
_instance = DjangoCemplateImporter()

if _instance is not None:
    sys.meta_path.append(_instance)
