# src/project_biophilia/services/__init__.py

from .weather_client import fetchCurrentWeather

# Optional: Define __all__ to explicitly control what gets exported
__all__ = ["fetchCurrentWeather"]
