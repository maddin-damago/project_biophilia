from fastapi import APIRouter, HTTPException  # ,HTTPException
from pydantic import BaseModel
from typing import Literal


# Define the structure of the data you expect from the user
class User_Mood(BaseModel):
    energy_level: Literal["low", "mid", "high"]
    age: int


router = APIRouter(prefix="/api", tags=["User & Mood"])

temporary_mood_storage: dict[str, User_Mood] = {}


@router.post("/user-mood")
async def getUserMood(user_mood: User_Mood) -> dict[str, str | User_Mood]:
    temporary_mood_storage["latest"] = user_mood
    return {"message": "Mood successfully cached in RAM", "data": temporary_mood_storage["latest"]}


@router.get("/user-mood/latest")
async def get_latest_mood():
    # Fetch the data back out of RAM

    latest_data = temporary_mood_storage.get("latest")

    if not latest_data:
        raise HTTPException(
            status_code=404, detail="No mood data submitted yet")

    return latest_data
