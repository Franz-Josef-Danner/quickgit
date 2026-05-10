# QuickGit auf Windows per Doppelklick starten

Wenn sich `.py`-Dateien beim Doppelklick im Editor öffnen, ist die Dateizuordnung in Windows auf den Editor gesetzt.

## Empfohlener Weg (ohne Umstellen der globalen Dateizuordnung)
1. Doppelklicke `start_quickgit_ui.bat`.
2. Die Batch-Datei versucht automatisch in dieser Reihenfolge zu starten:
   - `pyw quickgit_ui.pyw`
   - `pythonw quickgit_ui.pyw`
   - `python quickgit_ui.pyw` (mit Konsole)

So funktioniert der Start auch dann, wenn `pyw` auf deinem System fehlt.

## Alternative: `.pyw` mit Python verknüpfen
1. Rechtsklick auf `quickgit_ui.pyw` → **Öffnen mit** → **Andere App auswählen**.
2. **Python Launcher (pyw.exe)** auswählen.
3. Haken setzen bei **Immer diese App zum Öffnen von .pyw-Dateien verwenden**.

Danach kannst du `quickgit_ui.pyw` per Doppelklick starten (ohne Konsolenfenster).

## Wenn Python noch nicht sauber verknüpft ist
- Installiere Python von https://www.python.org/downloads/windows/
- Bei der Installation aktivieren:
  - **Add python.exe to PATH**
  - **Install launcher for all users (recommended)**

## Hinweis zur `.py`-Verknüpfung
Du kannst auch `.py` wieder auf Python umstellen, aber das betrifft **alle** Python-Dateien systemweit. Deshalb ist `start_quickgit_ui.bat` in der Praxis oft die bessere Lösung.
