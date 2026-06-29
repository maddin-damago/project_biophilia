# src/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.project_biophilia.api.weather_router import router as weather_router
from src.project_biophilia.api.user_mood_router import router as user_mood_router
from src.project_biophilia.api.recommendation_router import router as recommendation_router
# from src.api.herbs_router import router as herbs_router  <-- Your team can add this tomorrow!

app = FastAPI(title="Biophilia & Wild Herbs API")

app.add_middleware(
    CORSMiddleware,
    # The default port your Vite React app runs on
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],                      # Allows GET, POST, OPTIONS, etc.
    allow_headers=["*"],                      # Allows standard headers
)

# Mount your router paths
app.include_router(weather_router)
app.include_router(user_mood_router)
app.include_router(recommendation_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Biophilia & Mood API. Head over to /docs for interactive testing!"}
