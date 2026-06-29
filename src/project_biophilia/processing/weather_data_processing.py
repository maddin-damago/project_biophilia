# from ..services.weather_client import fetchCurrentWeather

from weather_client_2 import fetchCurrentWeather

import pandas as pd

from astral import LocationInfo
from astral.sun import sun

from datetime import timezone


# from ..helpers import print_my_data


# hier kriegt man die wetterdaten und speichert sie in einer variablen für 52.52... -> Berlin
weather_data = fetchCurrentWeather(52.52, 13.42)
print("tt", weather_data)

weather_data['date'] = pd.to_datetime(
    weather_data['date'] + pd.Timedelta(days=0, hours=2, minutes=0), utc=False)
print("tt2", weather_data)

# datum automatisch aus den daten holen
current_date = weather_data['date'].dt.date.iloc[0]

# standort definieren
city = LocationInfo("Berlin", "Germany", "Europe/Berlin", 52.52, 13.42)
s = sun(city.observer, date=current_date, tzinfo=city.timezone)


sunrise_utc = s['sunrise'].astimezone(
    timezone.utc).replace(minute=0, second=0, microsecond=0)
sunrise_utc += pd.Timedelta(days=0, hours=2, minutes=0)
sunset_utc = s['sunset'].astimezone(timezone.utc).replace(
    minute=0, second=0, microsecond=0)
sunset_utc += pd.Timedelta(days=0, hours=2, minutes=0)


df_day = weather_data[(weather_data['date'] >= sunrise_utc)
                      & (weather_data['date'] <= sunset_utc)]

print(df_day)

print(sunrise_utc)
print(sunset_utc)
# print(f"s:{s}")

# print(weather_data['date'].head(10))
# print(weather_data['date'].dtype)

weather_data['date'] = pd.to_datetime(weather_data['date'], utc=True)
# print(weather_data['temperature_2m'].min())
# print(weather_data['temperature_2m'].max())


def weatherDataProcessing():
    pass
    # alle_temps = weather_data["temperature_2m"]
   # weather_data = fetchCurrentWeather(52.52, 13.42)

    # print_my_data("heey hier", alle_temps)

    # print("meine daten von dulares", weather_data)


# @dataclass
# def temperature_score(self):

print(weather_data.columns.tolist())
