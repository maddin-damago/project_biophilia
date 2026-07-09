import json
from pathlib import Path


def generiereAktivitaet(stimmung_wetter_lage):
    current_dir = Path(__file__).resolve().parent
    file_path_handlungsempfehlungen = current_dir.parent / \
        "assets" / "handlungsempfehlungen.json"
    file_path_kraeuter = current_dir.parent / "assets" / "kraeuter.json"

    # JSON Dateien einlesen
    with open(file_path_handlungsempfehlungen, "r", encoding="utf-8") as f:
        handlungsempfehlungen_daten = json.load(f)

    with open(file_path_kraeuter, "r", encoding="utf-8") as f:
        kraeuter_daten = json.load(f)

    # Aktuelle Stimmung-Wetter-Lage aus Datei auslesen
    aktueller_fall = handlungsempfehlungen_daten[stimmung_wetter_lage]

    # 3. Pflanzennamen und Erläuterungen holen
    kraeuter_namen = []
    kraeuter_details_liste = []

    for kraeuter in aktueller_fall["kraeuter"]:
        pflanzen_details = kraeuter_daten[kraeuter]

        kraeuter_details_liste.append(pflanzen_details)

        kraeuter_namen.append(pflanzen_details["trivialName"])

    # Kräuternamen als schönen Text ausgeben:
    if len(kraeuter_namen) > 1:
        pflanzen_aufzaehlung = ", ".join(
            kraeuter_namen[:-1]) + " und " + kraeuter_namen[-1]
    else:
        pflanzen_aufzaehlung = kraeuter_namen

    ueberleitung_text = f"Als leiser Wegweiser zu deiner inneren Natur dürfen dich heute {pflanzen_aufzaehlung} begleiten. Nimm dir einen Moment Zeit, um dich mit der lebendigen Kraft dieser Wildkräuter zu verbinden:"

    return {
        "fall": stimmung_wetter_lage,
        "condition": aktueller_fall["condition"],
        "kraeuter_einleitung": ueberleitung_text,
        "kraeuter_details": kraeuter_details_liste,
        "aktivität": aktueller_fall["aktivität"],
        "erklaerung": aktueller_fall["erklaerung"]
    }


# ======================================================================
# NUR ZUM TESTEN (Diesen Teil zum Ausführen nutzen)
# ======================================================================
if __name__ == "__main__":
    test_stimmung_wetter_lage = "REDUCED_OUTDOOR"
    # oder: HIGH_INDOOR, STABLE_OUTDOOR, STABLE_INDOOR, REDUCED_OUTDOOR, REDUCED_INDOOR, CRITICAL_OUTDOOR, CRITICAL_INDOOR
    test_ergebnis = generiereAktivitaet(test_stimmung_wetter_lage)

    print("--- DEIN BIOPHILIA TEST-ERGEBNIS ---")
    print(json.dumps(test_ergebnis, indent=2, ensure_ascii=False))
