import numpy as np
from typing import Any
from dataclasses import dataclass


# Types


@dataclass
class WeatherScore:
    # All sub-scores (0–100) and the final combined score
    sunshine_score: float
    temperature_score: float
    humidity_score: float
    precipitation_score: float
    uv_score: float
    cloud_score: float
    combined_score: float       # weighted average of all sub-scores


@dataclass
class ActivityCategory:
    """One of the 8 output categories."""
    environment: str            # "outdoor" | "indoor"
    level: str                  # "high" | "stable" | "reduced" | "critical"
    label: str                  # human-readable
    description: str
    score: float                # the combined 0-100 score that triggered this
    recommendations: list[str]


# ---------------------------------------------------------------------------
# Sub-score calculators (each returns 0–100)
# ---------------------------------------------------------------------------

def _score_temperature(temps: np.ndarray) -> float:
    """
    Optimal range 18–22 °C → 100.
    Drops off linearly outside that window.
    Below 0 °C or above 38 °C → 0.
    """
    avg = float(np.mean(temps))
    if 18 <= avg <= 22:
        return 100.0
    if avg < 18:
        return max(0.0, 100.0 - (18 - avg) * 5)
    # avg > 22
    return max(0.0, 100.0 - (avg - 22) * 5)


def _score_precipitation(precip_prob: np.ndarray) -> float:
    """
    0 % rain probability → 100.
    100 % probability → 0.
    """
    avg = float(np.mean(precip_prob))
    return max(0.0, 100.0 - avg)


def _score_cloud_cover(clouds: np.ndarray) -> float:
    """
    0 % cloud cover → 100 (clear sky).
    100 % overcast → 20 (not 0 – diffuse light still has value).
    """
    avg = float(np.mean(clouds))
    return max(20.0, 100.0 - avg * 0.8)


def _score_uv(uv: np.ndarray) -> float:
    """
    UV index 3–5 → 100 (healthy exposure).
    UV > 8 → penalty (risk of sunburn).
    UV < 1 → low score (little benefit).
    """
    avg = float(np.mean(uv))
    if avg < 1:
        return 30.0
    if 1 <= avg < 3:
        return 60.0 + (avg - 1) * 20        # 60 → 100
    if 3 <= avg <= 5:
        return 100.0
    if 5 < avg <= 8:
        return max(60.0, 100.0 - (avg - 5) * 13.3)
    # avg > 8 — high UV risk
    return max(20.0, 60.0 - (avg - 8) * 10)


def _score_humidity(humidity: np.ndarray) -> float:
    """
    Optimal 40–60 % → 100.
    < 30 % or > 70 % → discomfort.
    """
    avg = float(np.mean(humidity))
    if 40 <= avg <= 60:
        return 100.0
    if avg < 40:
        return max(0.0, 100.0 - (40 - avg) * 3.3)
    # avg > 60
    return max(0.0, 100.0 - (avg - 60) * 3.3)


# ---------------------------------------------------------------------------
# Combined score
# ---------------------------------------------------------------------------

# Weights must sum to 1.0
_WEIGHTS = {
    "temperature":   0.25,
    "precipitation": 0.30,   # highest – rain is the biggest blocker
    "cloud_cover":   0.15,
    "uv":            0.15,
    "humidity":      0.15,
}


def calculate_weather_score(weather_data: dict[str, Any]) -> WeatherScore:
    temps = np.array(weather_data["temperature_2m"],           dtype=float)
    precip = np.array(weather_data["precipitation_probability"], dtype=float)
    clouds = np.array(weather_data["cloud_cover"],              dtype=float)
    uv = np.array(weather_data["uv_index"],                 dtype=float)
    humidity = np.array(weather_data["relative_humidity_2m"],     dtype=float)

    t_score = _score_temperature(temps)
    p_score = _score_precipitation(precip)
    c_score = _score_cloud_cover(clouds)
    u_score = _score_uv(uv)
    h_score = _score_humidity(humidity)

    combined = (
        t_score * _WEIGHTS["temperature"] +
        p_score * _WEIGHTS["precipitation"] +
        c_score * _WEIGHTS["cloud_cover"] +
        u_score * _WEIGHTS["uv"] +
        h_score * _WEIGHTS["humidity"]
    )

    return WeatherScore(
        sunshine_score=round(c_score, 1),       # proxy for sunshine
        temperature_score=round(t_score, 1),
        humidity_score=round(h_score, 1),
        precipitation_score=round(p_score, 1),
        uv_score=round(u_score, 1),
        cloud_score=round(c_score, 1),
        combined_score=round(combined, 1),
    )


# ---------------------------------------------------------------------------
# 8-category classifier
# ---------------------------------------------------------------------------
#
#  Score thresholds (weather-only, 0–100):
#
#   75–100  → outdoor  · high
#   55–74   → outdoor  · stable
#   35–54   → outdoor  · reduced   (or indoor stable depending on precip)
#   0–34    → outdoor  · critical  / forced indoor
#
#  The indoor counterpart is always one level "better" than the outdoor
#  reading because you're sheltered from the negative factors.
#
#  Final rule: if precipitation score < 40 (likely rain) the primary
#  recommendation flips to indoor regardless of the combined score.

def classify_activity(score: WeatherScore) -> ActivityCategory:
    s = score.combined_score
    rainy = score.precipitation_score < 40

    # ── Outdoor high ────────────────────────────────────────────────────────
    if s >= 75 and not rainy:
        return ActivityCategory(
            environment="outdoor",
            level="high",
            label="Outdoor · High",
            description="Ausgezeichnete Bedingungen – idealer Tag für intensive Outdoor-Aktivitäten.",
            score=s,
            recommendations=[
                "Längere Wanderungen oder Radtouren",
                "Sport im Freien (Laufen, Yoga im Park)",
                "Waldbaden / Shinrin-yoku",
                "Picknick oder Gartenarbeit",
            ],
        )

    # ── Outdoor stable ──────────────────────────────────────────────────────
    if 55 <= s < 75 and not rainy:
        return ActivityCategory(
            environment="outdoor",
            level="stable",
            label="Outdoor · Stable",
            description="Gute Bedingungen für moderate Outdoor-Aktivitäten.",
            score=s,
            recommendations=[
                "Spaziergang im Park oder Wald",
                "Leichtes Stretching / Atemübungen draußen",
                "Entspannte Fahrradtour",
                "Kurze Mittagspause im Freien",
            ],
        )

    # ── Outdoor reduced ─────────────────────────────────────────────────────
    if 35 <= s < 55 and not rainy:
        return ActivityCategory(
            environment="outdoor",
            level="reduced",
            label="Outdoor · Reduced",
            description="Mäßige Bedingungen – kurze Outdoor-Einheiten sind möglich, aber begrenzt.",
            score=s,
            recommendations=[
                "Kurzer Spaziergang (15–20 Min.)",
                "Bewusste Atemübungen an der frischen Luft",
                "Balkon- oder Terrassenzeit",
                "Leichte Gartenarbeit in geschützter Lage",
            ],
        )

    # ── Outdoor critical ────────────────────────────────────────────────────
    if s < 35 and not rainy:
        return ActivityCategory(
            environment="outdoor",
            level="critical",
            label="Outdoor · Critical",
            description="Ungünstige Bedingungen – Outdoor-Aktivitäten nur kurz und geschützt.",
            score=s,
            recommendations=[
                "Nur kurze Wege (Einkauf, etc.)",
                "Wetterfeste Kleidung anziehen",
                "Drinnen Tageslichtlampe nutzen",
                "Bewegung auf Indoor-Alternativen verlagern",
            ],
        )

    # ── Ab hier: Regen dominiert → Indoor-Kategorien ────────────────────────

    # ── Indoor high ─────────────────────────────────────────────────────────
    if s >= 65:
        return ActivityCategory(
            environment="indoor",
            level="high",
            label="Indoor · High",
            description="Trotz Regen hoher Wellbeing-Potenzial – perfekter Tag für produktive Indoor-Zeit.",
            score=s,
            recommendations=[
                "Intensives Home-Workout / Yoga",
                "Kreativer Flow-State (Zeichnen, Schreiben, Musik)",
                "Neue Rezepte ausprobieren",
                "Tiefes Lernprojekt starten",
            ],
        )

    # ── Indoor stable ───────────────────────────────────────────────────────
    if 45 <= s < 65:
        return ActivityCategory(
            environment="indoor",
            level="stable",
            label="Indoor · Stable",
            description="Gute Indoor-Bedingungen – strukturierter Tag mit Wohlbefinden-Fokus.",
            score=s,
            recommendations=[
                "Leichtes Home-Workout oder Stretching",
                "Meditationseinheit (10–20 Min.)",
                "Kräutertee trinken & bewusst pausieren",
                "Pflanzen gießen / Indoor-Natur pflegen",
            ],
        )

    # ── Indoor reduced ──────────────────────────────────────────────────────
    if 25 <= s < 45:
        return ActivityCategory(
            environment="indoor",
            level="reduced",
            label="Indoor · Reduced",
            description="Anspruchsvolle Bedingungen – regenerativer Indoor-Tag empfohlen.",
            score=s,
            recommendations=[
                "Ruhe & Erholung priorisieren",
                "Warme Mahlzeiten kochen (Suppen, Eintöpfe)",
                "Sanfte Atemübungen oder Body-Scan",
                "Tageslichtlampe einsetzen",
            ],
        )

    # ── Indoor critical ─────────────────────────────────────────────────────
    return ActivityCategory(
        environment="indoor",
        level="critical",
        label="Indoor · Critical",
        description="Sehr schlechte Außenbedingungen – vollständiger Indoor-Tag, Selbstfürsorge-Modus.",
        score=s,
        recommendations=[
            "Vollständige Ruhe & Regeneration",
            "Warme Getränke, Decke, Komfort-Routinen",
            "Leichte Stretching-Einheit auf der Matte",
            "Professionelle Hilfe suchen falls Stimmung anhaltend tief",
        ],
    )
