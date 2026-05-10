#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Erstellt eine .exe-Datei für das Large File .gitignore Generator Programm
Führe dieses Skript aus: python build_exe.py
"""

import subprocess
import sys

print("Installiere PyInstaller...")
subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

print("\nErstelle .exe-Datei...")
subprocess.check_call([
    sys.executable, "-m", "pyinstaller",
    "--onefile",
    "--windowed",
    "--name=QuickGit",
    "--distpath=.",
    "large_file_gitignore.py"
])

print("\n✅ Fertig! Die Datei 'QuickGit.exe' wurde erstellt.")
print("Du kannst sie jetzt auf den Desktop kopieren und doppelklicken!")
