# from src.project_biophilia.processing.weather_scoring import WeatherScore
from datetime import timezone
from astral.sun import sun
from astral import LocationInfo
import numpy as np
import pandas as pd
from src.project_biophilia.services.weather_client import fetchCurrentWeather
from src.project_biophilia.api.user_mood_router import get_latest_mood_summary


def weatherDataProcessing(latitude: float = 52.52, longitude: float = 13.42):
    # wetterdaten holen
    weather_data = fetchCurrentWeather(latitude, longitude)
    # print(weather_data)
    #
    mood_score = get_latest_mood_summary()

    # Fallback-Mittelwert falls der allererste Aufruf ohne gespeicherte Moods stattfindet
    assert mood_score is not None
    mood_sum = mood_score["sum"]
    mood_kat = "STABLE"

    # WHO-5 Klassifizierung
    if mood_sum >= 20:
        mood_kat = "HIGH"
    elif mood_sum >= 13:
        mood_kat = "STABLE"
    elif mood_sum >= 8:
        mood_kat = "REDUCED"
    else:
        mood_kat = "CRITICAL"

    print(mood_score)

    # datum korrigieren (UTC+2)
    # weather_data["date"] = pd.to_datetime(
    # weather_data["date"] + pd.Timedelta(hours=2), utc=False
    # )

    # sonnenaufgang/sonnenuntergang berechnen
    current_date = weather_data["date"].dt.date.iloc[2]
    city = LocationInfo("Berlin", "Germany",
                        "Europe/Berlin", latitude, longitude)
    sun_data = sun(city.observer, date=current_date, tzinfo=city.timezone)

    sunrise = sun_data["sunrise"].astimezone(timezone.utc).replace(
        minute=0, second=0, microsecond=0)
    sunrise += pd.Timedelta(hours=2)
    sunset = sun_data["sunset"].astimezone(timezone.utc).replace(
        minute=0, second=0, microsecond=0)
    sunset += pd.Timedelta(hours=2)

    # aktuelle tagesdaten filtern
    df_day = weather_data[
        (weather_data["date"] >= sunrise) &
        (weather_data["date"] <= sunset)
    ]

    # arrays für WeatherScore vorbereiten
    temps = df_day["temperature_2m"].to_numpy()
    # humidity = df_day["relative_humidity_2m"].to_numpy()
    # uv = df_day["uv_index"].to_numpy()
    # cloud = df_day["cloud_cover"].to_numpy()
    precip_prob = df_day["precipitation_probability"].to_numpy()

    avg_temp = float(np.mean(temps))
    avg_precip = float(np.mean(precip_prob))

    stimmung_wetter_lage = "OUTDOOR"
    warnings = []

    if avg_precip >= 50.0:
        stimmung_wetter_lage = "INDOOR"
        warnings.append("f Hohe Regenwahrscheinlichkeit({avg_precip: .0f}%)")

    elif avg_temp < 10.0:
        stimmung_wetter_lage = "INDOOR"
        warnings.append("f Schutz vor Kälte({avg_temp:.1f}°C)")

    elif avg_temp > 35.0:
        stimmung_wetter_lage = "INDOOR"
        warnings.append("f Schutz vor extremer Hitze({avg_temp:.1f}°C)")

    # optionaler WeatherScore punktestand für das UI/warnungen
   # scorer = WeatherScore()
   # final_score, score_warnings = scorer.combined_score(
       # temps, humidity, uv, cloud)
    # warnings.extend(score_warnings)

    recommendation_key = mood_kat + "_" + stimmung_wetter_lage
    print(recommendation_key)
    return recommendation_key


if __name__ == "__main__":
    result = weatherDataProcessing()

    # print(result)
