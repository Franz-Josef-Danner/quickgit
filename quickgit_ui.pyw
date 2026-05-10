#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Windows GUI-Einstiegspunkt ohne Konsole für QuickGit.

Bei Fehlern wird ein Logfile geschrieben und eine Meldung angezeigt,
damit stille Abstuerze bei .pyw-Start sichtbar werden.
"""

from pathlib import Path
import traceback
import ctypes

from quickgit_ui import main


def show_error(message: str):
    try:
        ctypes.windll.user32.MessageBoxW(0, message, "QuickGit Fehler", 0x10)
    except Exception:
        pass


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        log_path = Path(__file__).with_name("quickgit_error.log")
        details = traceback.format_exc()
        log_path.write_text(details, encoding="utf-8")
        show_error(
            "QuickGit ist beim Start abgestuerzt.\n\n"
            f"Fehler: {exc}\n\n"
            f"Details in: {log_path}"
        )
