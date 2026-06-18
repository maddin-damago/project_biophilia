
from fastapi import APIRouter, HTTPException
from src.project_biophilia.services.weather_client import fetchCurrentWeather
import numpy as np
from typing import Any, cast

router = APIRouter(prefix="/api/weather", tags=["Weather & Mood"])


@router.get("/mood-index")
def get_biophilic_mood_index(lat: float = 52.52, lon: float = 13.41) -> dict[str, Any]:
    try:
        # Call your incoming service!
        weather_data = fetchCurrentWeather(lat, lon)

        # Calculate mean values from your NumPy arrays for the day
        avg_clouds = float(cast(float, np.mean(weather_data["cloud_cover"])))
        avg_sun = float(
            cast(float, np.mean(weather_data["shortwave_radiation"])))

        # A simple, fun formula for your classmates' mood index
        if avg_sun > 150 and avg_clouds < 30:
            mood_status = "Excellent - Perfect environment for outdoor forest bathing!"
        elif avg_clouds > 75:
            mood_status = "Melancholic - Great day to stay inside with Chamomile tea."
        else:
            mood_status = "Balanced - Good conditions for a nature walk."

        return {
            "location": {"latitude": lat, "longitude": lon},
            "average_cloud_cover_percent": round(avg_clouds, 1),
            "average_sunlight_w_m2": round(avg_sun, 1),
            "biophilia_mood_index": mood_status
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to calculate mood index: {str(e)}")
