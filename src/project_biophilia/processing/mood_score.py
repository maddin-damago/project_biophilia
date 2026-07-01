from src.project_biophilia.api.user_mood_router import get_latest_mood_summary
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
# 3 ebenen hochgehen um im hauptverzeichnis (project_biophilia) zu landen
project_root = os.path.abspath(os.path.join(current_dir, "../../.."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


mood_score = get_latest_mood_summary()

print(mood_score)

if mood_score is not None:
    echte_summe = mood_score["sum"]
    print(f"Erfolgreich! Die echte Summe für deine Matrix ist: {echte_summe}")
else:
    print("Keine Daten gefunden. Bitte sende zuerst Daten mit Bruno ab.")
