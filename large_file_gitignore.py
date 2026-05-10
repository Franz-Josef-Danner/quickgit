#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Large File .gitignore Generator
Ein einfaches Programm für Windows 11, das große Dateien findet
und automatisch .gitignore Dateien in den jeweiligen Ordnern erstellt.
"""

import os
import sys
from pathlib import Path
from tkinter import Tk, Text, filedialog, messagebox
from tkinter import ttk
import threading


class LargeFileGitignoreApp:
    """Hauptanwendung zur Verwaltung großer Dateien und .gitignore Erstellung"""
    
    def __init__(self, root):
        """Initialisiert die Anwendung"""
        self.root = root
        self.root.title("QuickGit - Large File .gitignore Generator")
        self.root.geometry("700x620")
        self.root.resizable(False, False)
        
        # Versuche, Icon zu setzen (optional)
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
        
        # Erstelle GUI-Elemente
        self.selected_folder = None
        self.large_files_by_folder = {}
        self.gitignore_count = 0
        self.size_limit_mb = 100  # Standardwert
        
        self.create_widgets()
    
    def create_widgets(self):
        """Erstellt die Benutzeroberfläche"""
        # Titel
        title_label = ttk.Label(
            self.root, 
            text="QuickGit - Ordner-Scanner für große Dateien",
            font=("Arial", 14, "bold")
        )
        title_label.pack(pady=10)
        
        # Beschreibung
        description_text = (
            "Dieses Programm findet alle Dateien größer als die angegebene Größe\n"
            "und erstellt .gitignore Dateien in den jeweiligen Ordnern."
        )
        desc_label = ttk.Label(
            self.root,
            text=description_text,
            font=("Arial", 10),
            justify="center"
        )
        desc_label.pack(pady=5)
        
        # Ordner-Auswahl
        folder_frame = ttk.LabelFrame(self.root, text="Ordner auswählen", padding=10)
        folder_frame.pack(pady=10, padx=10, fill="x")
        
        select_button = ttk.Button(
            folder_frame,
            text="📁 Ordner durchsuchen",
            command=self.select_folder,
            width=30
        )
        select_button.pack(side="left", padx=5)

        # Status-Anzeige
        self.status_label = ttk.Label(
            folder_frame,
            text="Kein Ordner ausgewählt",
            font=("Arial", 9),
            foreground="gray"
        )
        self.status_label.pack(side="left", padx=10)
        
        # Dateigröße-Eingabe
        size_frame = ttk.LabelFrame(self.root, text="Dateigröße (optional)", padding=10)
        size_frame.pack(pady=10, padx=10, fill="x")
        
        size_label = ttk.Label(size_frame, text="Mindestgröße in MB:")
        size_label.pack(side="left", padx=5)
        
        self.size_entry = ttk.Entry(size_frame, width=10)
        self.size_entry.insert(0, "100")  # Standardwert
        self.size_entry.pack(side="left", padx=5)
        
        mb_label = ttk.Label(size_frame, text="MB (z.B. 50, 100, 500)")
        mb_label.pack(side="left", padx=5)

        self.scan_button = ttk.Button(
            size_frame,
            text="▶ Scan starten",
            command=self.start_scan,
            state="disabled"
        )
        self.scan_button.pack(side="right", padx=5)
        
        # Fortschrittsanzeige
        self.progress_bar = ttk.Progressbar(
            self.root,
            mode="indeterminate",
            length=400
        )
        self.progress_bar.pack(pady=10)

        # Log-Ausgabe
        log_frame = ttk.LabelFrame(self.root, text="Log", padding=5)
        log_frame.pack(pady=(0, 10), padx=10, fill="x")

        self.log_text = Text(log_frame, height=4, wrap="word")
        self.log_text.pack(fill="x")
        self.log_text.config(state="disabled")

        # Text-Ausgabe für Ergebnisse
        self.result_frame = ttk.LabelFrame(self.root, text="Ergebnisse", padding=5)
        self.result_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Scrollbare Text-Anzeige
        scrollbar = ttk.Scrollbar(self.result_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.result_text = ttk.Treeview(
            self.result_frame,
            height=8,
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.result_text.yview)
        self.result_text.pack(side="left", fill="both", expand=True)
        
        # Buttons im unteren Bereich
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)
        
        close_button = ttk.Button(
            button_frame,
            text="Beenden",
            command=self.root.quit
        )
        close_button.pack(side="left", padx=5)

        self.append_log("Anwendung gestartet. Bitte Ordner auswählen.")
    
    def append_log(self, message):
        """Schreibt eine Zeile in die Log-Ausgabe"""
        self.log_text.config(state="normal")
        self.log_text.insert("end", f"{message}\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")

    def select_folder(self):
        """Öffnet den Ordner-Auswahldialog"""
        folder = filedialog.askdirectory(title="Wählen Sie einen Ordner aus")
        if folder:
            self.selected_folder = folder
            self.status_label.config(
                text=f"✅ {folder}",
                foreground="green"
            )
            self.scan_button.config(state="normal")
            self.result_text.delete(*self.result_text.get_children())
            self.large_files_by_folder = {}
            self.gitignore_count = 0
            self.append_log(f"Ordner ausgewählt: {folder}")
            self.append_log("Scan-Button ist jetzt aktiv. Du kannst den Scan starten.")

    def start_scan(self):
        """Startet den Scan in einem separaten Thread"""
        if not self.selected_folder:
            messagebox.showwarning("Fehler", "Bitte wählen Sie erst einen Ordner aus!")
            return

        # Validiere die Eingabe
        try:
            self.size_limit_mb = int(self.size_entry.get())
            if self.size_limit_mb <= 0:
                raise ValueError("Größe muss größer als 0 sein")
        except ValueError:
            messagebox.showerror("Fehler", "Bitte geben Sie eine gültige Zahl ein (z.B. 100)")
            return
        
        self.scan_button.config(state="disabled")
        self.progress_bar.start()
        self.append_log(f"Scan gestartet (Grenze: {self.size_limit_mb} MB)...")
        
        # Starten des Scans in einem Thread, um die GUI nicht einzufrieren
        scan_thread = threading.Thread(target=self.perform_scan)
        scan_thread.start()
    
    def perform_scan(self):
        """Führt den Scan durch und erstellt .gitignore Dateien"""
        try:
            self.large_files_by_folder = {}
            
            # Finde alle Dateien größer als die angegebene Größe
            self.find_large_files(self.selected_folder)
            
            # Erstelle .gitignore Dateien
            self.gitignore_count = 0
            for folder, files in self.large_files_by_folder.items():
                self.create_gitignore(folder, files)
            
            # Zeige Ergebnisse
            self.display_results()
            
            # Zeige Erfolgs-Meldung
            message = (
                f"Scan abgeschlossen!\n\n"
                f"Große Dateien gefunden in {len(self.large_files_by_folder)} Ordner(n)\n"
                f".gitignore Dateien erstellt: {self.gitignore_count}"
            )
            self.root.after(0, lambda: messagebox.showinfo("Erfolg", message))
            self.root.after(0, lambda: self.append_log("Scan erfolgreich abgeschlossen."))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten:\n{str(e)}"))
            self.root.after(0, lambda: self.append_log(f"Fehler: {e}"))
        
        finally:
            self.progress_bar.stop()
            self.scan_button.config(state="normal")
    
    def find_large_files(self, start_path):
        """Durchsucht den Ordner rekursiv nach großen Dateien"""
        size_limit_bytes = self.size_limit_mb * 1024 * 1024
        
        try:
            for root, dirs, files in os.walk(start_path):
                # Ignoriere .git Ordner
                if ".git" in dirs:
                    dirs.remove(".git")
                
                large_files = []
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        file_size = os.path.getsize(file_path)
                        if file_size > size_limit_bytes:
                            large_files.append(file)
                    except (OSError, IOError):
                        pass
                
                # Speichere Ordner mit großen Dateien
                if large_files:
                    self.large_files_by_folder[root] = large_files
        
        except Exception as e:
            raise Exception(f"Fehler beim Durchsuchen der Ordner: {str(e)}")
    
    def create_gitignore(self, folder, files):
        """Erstellt oder aktualisiert die .gitignore Datei"""
        gitignore_path = os.path.join(folder, ".gitignore")
        
        try:
            # Lese existierende Einträge
            existing_entries = set()
            if os.path.exists(gitignore_path):
                with open(gitignore_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            existing_entries.add(line)
            
            # Neue Einträge hinzufügen
            new_entries = set(files) - existing_entries
            
            if new_entries:
                with open(gitignore_path, "a", encoding="utf-8") as f:
                    if os.path.getsize(gitignore_path) > 0:
                        f.write("\n")
                    for file in sorted(new_entries):
                        f.write(f"{file}\n")
                
                self.gitignore_count += 1
        
        except Exception as e:
            raise Exception(f"Fehler beim Erstellen von .gitignore in {folder}: {str(e)}")
    
    def display_results(self):
        """Zeigt die Ergebnisse in der Benutzeroberfläche an"""
        # Lösche alte Einträge
        for item in self.result_text.get_children():
            self.result_text.delete(item)
        
        # Zeige neue Ergebnisse
        if not self.large_files_by_folder:
            self.result_text.insert("", "end", text=f"Keine Dateien größer als {self.size_limit_mb} MB gefunden.")
            return
        
        for folder in sorted(self.large_files_by_folder.keys()):
            files = self.large_files_by_folder[folder]
            folder_id = self.result_text.insert("", "end", text=f"📁 {folder}")
            
            for file in sorted(files):
                try:
                    file_path = os.path.join(folder, file)
                    size_mb = os.path.getsize(file_path) / (1024 * 1024)
                    self.result_text.insert(folder_id, "end", text=f"  📄 {file} ({size_mb:.1f} MB)")
                except:
                    self.result_text.insert(folder_id, "end", text=f"  📄 {file}")


def main():
    """Haupteinstiegspunkt"""
    root = Tk()
    app = LargeFileGitignoreApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
