from importlib import import_module
from types import ModuleType

import pytest


def load_module(module_path: str) -> ModuleType:
    try:
        return import_module(module_path)
    except ModuleNotFoundError as exc:
        pytest.fail(f"brak {module_path}: {exc}")


def load_attr(module_path: str, name: str) -> object:
    try:
        return getattr(load_module(module_path), name)
    except AttributeError as exc:
        pytest.fail(f"brak {module_path}.{name}: {exc}")
