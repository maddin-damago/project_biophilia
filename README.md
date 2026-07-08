# Project Biophilia

Anwendung die aufgrund von Wetterdaten und Energielevel einen Mood Score und eine Empfehlung von Wildkräutern/Naturerfahrung gibt. Der Nutzer füllt zunächst einen kleinen Fragebogen aus, dieser wird von der Anwendung verarbeitet und gibt eine Empfehlung zurück.

## Prerequisites
Python 3.12+

## How to set the project up

1. Clone the repo: `git clone https://github.com/maddin-damago/project_biophilia.git`
2. Change into the repository directory: `cd project_biophilia`
3. Install dependencies: `pip install -r requirements.txt`
4. Start the server: `uvicorn src.project_biophilia.main:app --reload` or `python3 -m uvicorn src.project_biophilia.main:app --reload`
   > 💡 **Windows 11 Tip:** If PowerShell gives you a red "Running Scripts is disabled" error when starting Uvicorn, open PowerShell as Administrator and run:
   > `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
5. Use the server at `127.0.0.1:8000`
6. Find the API Docu at `127.0.0.1:8000/docs`
