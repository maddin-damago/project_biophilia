# src/main.py
from fastapi import FastAPI
from src.project_biophilia.api.weather_router import router as weather_router
from src.project_biophilia.api.user_mood_router import router as user_mood_router
# from src.api.herbs_router import router as herbs_router  <-- Your team can add this tomorrow!

app = FastAPI(title="Biophilia & Wild Herbs API")

# Mount your router paths
app.include_router(weather_router)
app.include_router(user_mood_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Biophilia & Mood API. Head over to /docs for interactive testing!"}
