import math

import openmeteo_requests
import pandas as pd
import niquests  # <-- Use niquests instead of requests / requests_cache
from typing import List, Any
import numpy as np

from ..helpers import print_my_data

# Import underlying openmeteo types
from openmeteo_sdk.WeatherApiResponse import WeatherApiResponse

# Create a native niquests Session (fully compatible with openmeteo out-of-the-box)
# niquests handles retries and pooling natively!
session = niquests.Session()

# Pass it straight to the client without needing any type casting
openmeteo = openmeteo_requests.Client(session=session)

# Define a precise type alias for the NumPy arrays
FloatArray = np.ndarray[Any, np.dtype[np.float32]]


def fetchCurrentWeather(lat: float, long: float):
    url: str = "https://api.open-meteo.com/v1/forecast"
    params: dict[str, float | list[str] | str] = {
        "latitude": lat,
        "longitude": long,
        "forecast_days": 1,
        "timezone": "Europe/Berlin",
        "hourly": [
            "temperature_2m",
            "precipitation_probability",
            "cloud_cover",
            "uv_index",
            "relative_humidity_2m"
        ]  # ,
        # "models": "icon_seamless",
    }

    responses: List[WeatherApiResponse] = openmeteo.weather_api(  # type: ignore[reportUnknownMemberType]
        url, params=params)
    response: WeatherApiResponse = responses[0]

    print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation: {response.Elevation()} m asl")
    print(f"Timezone: {response.Timezone()}{response.TimezoneAbbreviation()}")
    print(
        f"Timezone difference to GMT+0: {response.UtcOffsetSeconds() / 3600}h")

    # Process hourly data
    hourly = response.Hourly()
    if hourly is None:
        raise ValueError("No hourly data returned from the API")

    # Add a helper function to safely extract variables and satisfy Pylance

    def get_hourly_var(index: int) -> FloatArray:
        # The "Bang" setup
        assert hourly is not None
        var = hourly.Variables(index)
        if var is None:
            raise ValueError(
                f"Requested weather variable at index {index} is missing from the API response.")
        return var.ValuesAsNumpy()

    # Cleanly extract your data with ZERO Pylance warnings!
    hourly_temperature_2m: FloatArray = get_hourly_var(0)
    hourly_precipitation_probability: FloatArray = get_hourly_var(1)
    hourly_cloud_cover: FloatArray = get_hourly_var(2)
    hourly_uv_index: FloatArray = get_hourly_var(3)
    hourly_relative_humidity_2m: FloatArray = get_hourly_var(4)

    hourly_data: dict[str, Any] = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        )
    }

    hourly_data["temperature_2m"] = hourly_temperature_2m
    hourly_data["precipitation_probability"] = hourly_precipitation_probability
    hourly_data["cloud_cover"] = hourly_cloud_cover
    hourly_data["uv_index"] = hourly_uv_index
    hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m

    hourly_dataframe: pd.DataFrame = pd.DataFrame(  # type: ignore
        data=hourly_data)

    print_my_data("What is fetched:", hourly_data)
    return hourly_data
