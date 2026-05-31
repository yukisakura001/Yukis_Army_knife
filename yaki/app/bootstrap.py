"""GUI startup for Yukis_Army_knife."""

import json
from pathlib import Path

from yaki.imports import *
from yaki.widgets import Tk
from yaki.app.common import (
    check_new_ver,
    esc_key_pressed,
    listener_window,
    make_folder,
    taskarea,
)
from yaki.app.shell import set_frame1

_STARTUP_BODY = Path(__file__).with_name("_startup_body.py")


def run_startup(ns: dict) -> None:
    source = _STARTUP_BODY.read_text(encoding="utf-8")
    exec(compile(source, str(_STARTUP_BODY), "exec"), ns, ns)