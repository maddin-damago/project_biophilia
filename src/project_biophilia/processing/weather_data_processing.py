from weather_client_2 import fetchCurrentWeather
from weather_scoring import WeatherScore

import pandas as pd
import numpy as np
from astral import LocationInfo
from astral.sun import sun
from datetime import timezone


def weatherDataProcessing(latitude: float = 52.52, longitude: float = 13.42) -> dict:
    # wetterdaten holen
    weather_data = fetchCurrentWeather(latitude, longitude)

    # datum korrigieren (UTC+2)
    weather_data['date'] = pd.to_datetime(
        weather_data['date'] + pd.Timedelta(hours=2), utc=False
    )

    # sonnenaufgang/sonnenuntergang berechnen
    current_date = weather_data['date'].dt.date.iloc[0]
    city = LocationInfo("Berlin", "Germany",
                        "Europe/Berlin", latitude, longitude)
    sun_data = sun(city.observer, date=current_date, tzinfo=city.timezone)
    print(sun_data)
    sunrise = sun_data['sunrise'].astimezone(timezone.utc).replace(
        minute=0, second=0, microsecond=0)
    sunrise += pd.Timedelta(hours=2)
    sunset = sun_data['sunset'].astimezone(timezone.utc).replace(
        minute=0, second=0, microsecond=0)
    sunset += pd.Timedelta(hours=2)

    # aktuelle tagesdaten filtern
    df_day = weather_data[
        (weather_data['date'] >= sunrise) &
        (weather_data['date'] <= sunset)
    ]

    # arrays für WeatherScore vorbereiten
    temps = df_day['temperature_2m'].to_numpy()
    humidity = df_day['relative_humidity_2m'].to_numpy()
    uv = df_day['uv_index'].to_numpy()
    cloud = df_day['cloud_cover'].to_numpy()

    # score berechnen
    scorer = WeatherScore()
    final_score, warnings = scorer.combined_score(temps, humidity, uv, cloud)

    return {
        "score": round(final_score, 1),
        "warnings": warnings
    }


if __name__ == "__main__":
    result = weatherDataProcessing()
    print(f"Mood Index: {result['score']}/100")
    for w in result['warnings']:
        print(w)
