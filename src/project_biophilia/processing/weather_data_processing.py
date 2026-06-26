from ..services import fetchCurrentWeather
from ..helpers import print_my_data

weather_data = fetchCurrentWeather(52.52, 13.42)
print_my_data("meine daten", weather_data)


def weatherDataProcessing():

    # alle_temps = weather_data["temperature_2m"]
   # weather_data = fetchCurrentWeather(52.52, 13.42)

    # print_my_data("heey hier", alle_temps)

    # print("meine daten von dulares", weather_data)
