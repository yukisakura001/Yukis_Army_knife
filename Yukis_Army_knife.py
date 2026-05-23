# -*- coding: utf-8 -*-
"""Yukis_Army_knife entry point."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

_PKG_ROOT = Path(__file__).resolve().parent
if str(_PKG_ROOT) not in sys.path:
    sys.path.insert(0, str(_PKG_ROOT))

_LOAD_ORDER = (
    "yaki.imports",
    "yaki.widgets",
    "yaki.app.common",
    "yaki.features.tools",
    "yaki.app.shell",
)
_SYNC_BACK = ("yaki.app.common", "yaki.features.tools", "yaki.widgets")


def _merged_startup_namespace() -> dict:
    shell = importlib.import_module("yaki.app.shell")
    ns = shell.__dict__
    for mod_name in _LOAD_ORDER:
        mod = importlib.import_module(mod_name)
        if mod is shell:
            continue
        for key, value in mod.__dict__.items():
            if not key.startswith("_"):
                ns[key] = value
    for mod_name in _SYNC_BACK:
        mod = importlib.import_module(mod_name)
        mod.__dict__.update(
            {k: v for k, v in ns.items() if not k.startswith("_")}
        )
    return ns


def main() -> None:
    ns = _merged_startup_namespace()
    from yaki.app.bootstrap import run_startup

    run_startup(ns)


if __name__ == "__main__":
    main()
else:
    main()