#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Zentrale UI für QuickGit-Funktionen."""

import subprocess
import sys
import threading
from tkinter import Tk, StringVar, messagebox, ttk


class QuickGitLauncher:
    """Bedienerfreundlicher Launcher für vorhandene QuickGit-Skripte."""

    def __init__(self, root):
        self.root = root
        self.root.title("QuickGit - Bedienoberfläche")
        self.root.geometry("560x320")
        self.root.resizable(False, False)

        self.status_var = StringVar(value="Bereit")
        self.build_running = False

        self._create_widgets()

    def _create_widgets(self):
        title = ttk.Label(
            self.root,
            text="QuickGit - Zentrale Bedienoberfläche",
            font=("Arial", 14, "bold"),
        )
        title.pack(pady=(14, 8))

        desc = ttk.Label(
            self.root,
            text=(
                "Wähle eine Funktion per Klick aus.\n"
                "Du musst dafür keinen Code mehr anpassen."
            ),
            justify="center",
        )
        desc.pack(pady=(0, 14))

        frame = ttk.LabelFrame(self.root, text="Funktionen", padding=12)
        frame.pack(fill="x", padx=14)

        run_scanner_btn = ttk.Button(
            frame,
            text="🔍 Scanner UI öffnen",
            command=self.open_scanner_ui,
            width=28,
        )
        run_scanner_btn.grid(row=0, column=0, padx=6, pady=6)

        build_exe_btn = ttk.Button(
            frame,
            text="📦 Windows .exe bauen",
            command=self.build_exe,
            width=28,
        )
        build_exe_btn.grid(row=0, column=1, padx=6, pady=6)

        help_label = ttk.Label(
            frame,
            text=(
                "Scanner UI: startet die vorhandene Oberfläche zum Erstellen von .gitignore-Dateien.\n"
                "Windows .exe bauen: startet build_exe.py im Hintergrund."
            ),
            justify="left",
        )
        help_label.grid(row=1, column=0, columnspan=2, sticky="w", padx=6, pady=(8, 2))

        status_frame = ttk.LabelFrame(self.root, text="Status", padding=12)
        status_frame.pack(fill="x", padx=14, pady=14)

        status_label = ttk.Label(status_frame, textvariable=self.status_var)
        status_label.pack(anchor="w")

        close_btn = ttk.Button(self.root, text="Beenden", command=self.root.quit)
        close_btn.pack(pady=(0, 10))

    def open_scanner_ui(self):
        self.status_var.set("Starte Scanner UI...")
        try:
            subprocess.Popen([sys.executable, "large_file_gitignore.py"])
            self.status_var.set("Scanner UI gestartet")
        except Exception as exc:
            self.status_var.set("Fehler beim Start")
            messagebox.showerror("Fehler", f"Scanner UI konnte nicht gestartet werden:\n{exc}")

    def build_exe(self):
        if self.build_running:
            messagebox.showinfo("Hinweis", "Build läuft bereits.")
            return

        self.build_running = True
        self.status_var.set("Build gestartet. Das kann einige Minuten dauern...")

        def _run_build():
            try:
                process = subprocess.run(
                    [sys.executable, "build_exe.py"],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                if process.returncode == 0:
                    self.root.after(
                        0,
                        lambda: messagebox.showinfo(
                            "Erfolg", "Build abgeschlossen. 'QuickGit.exe' wurde erstellt."
                        ),
                    )
                    self.root.after(0, lambda: self.status_var.set("Build erfolgreich abgeschlossen"))
                else:
                    output = (process.stdout or "") + "\n" + (process.stderr or "")
                    self.root.after(
                        0,
                        lambda: messagebox.showerror(
                            "Build fehlgeschlagen",
                            f"build_exe.py meldete einen Fehler:\n\n{output.strip()}",
                        ),
                    )
                    self.root.after(0, lambda: self.status_var.set("Build fehlgeschlagen"))
            except Exception as exc:
                self.root.after(
                    0,
                    lambda: messagebox.showerror("Fehler", f"Build konnte nicht gestartet werden:\n{exc}"),
                )
                self.root.after(0, lambda: self.status_var.set("Fehler beim Build-Start"))
            finally:
                self.build_running = False

        threading.Thread(target=_run_build, daemon=True).start()


def main():
    root = Tk()
    QuickGitLauncher(root)
    root.mainloop()


if __name__ == "__main__":
    main()
