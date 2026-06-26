from fastapi import APIRouter, HTTPException
from src.project_biophilia import fetchCurrentWeather
from src.project_biophilia.processing.weather_scoring import (
    calculate_weather_score,
    classify_activity,
)
from typing import Any

router = APIRouter(prefix="/api/weather", tags=["Weather & Mood"])


@router.get("/mood-index")
def get_biophilic_mood_index(lat: float = 52.52, lon: float = 13.42) -> dict[str, Any]:
    """
    Returns weather sub-scores, a combined score (0–100),
    and one of 8 activity categories:
      outdoor · high / stable / reduced / critical
      indoor  · high / stable / reduced / critical
    """
    try:
        weather_data = fetchCurrentWeather(lat, lon)

        score    = calculate_weather_score(weather_data)
        category = classify_activity(score)

        return {
            "location": {
                "latitude": lat,
                "longitude": lon,
            },
            "scores": {
                "combined":      score.combined_score,
                "temperature":   score.temperature_score,
                "precipitation": score.precipitation_score,
                "cloud_cover":   score.cloud_score,
                "uv":            score.uv_score,
                "humidity":      score.humidity_score,
            },
            "category": {
                "environment":   category.environment,   # "outdoor" | "indoor"
                "level":         category.level,         # "high" | "stable" | "reduced" | "critical"
                "label":         category.label,
                "description":   category.description,
                "recommendations": category.recommendations,
            },
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to calculate mood index: {str(e)}",
        )


@router.get("/scores-only")
def get_scores_only(lat: float = 52.52, lon: float = 13.42) -> dict[str, Any]:
    """
    Lightweight endpoint – only scores, no category logic.
    Useful for the frontend chart/gauge.
    """
    try:
        weather_data = fetchCurrentWeather(lat, lon)
        score = calculate_weather_score(weather_data)

        return {
            "combined":      score.combined_score,
            "temperature":   score.temperature_score,
            "precipitation": score.precipitation_score,
            "cloud_cover":   score.cloud_score,
            "uv":            score.uv_score,
            "humidity":      score.humidity_score,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch scores: {str(e)}",
        )
