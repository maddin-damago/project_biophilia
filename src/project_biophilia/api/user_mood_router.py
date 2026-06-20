from fastapi import APIRouter  # ,HTTPException
from pydantic import BaseModel
from typing import Literal


# Define the structure of the data you expect from the user
class User_Mood(BaseModel):
    energy_level: Literal["low", "mid", "high"]
    age: int


router = APIRouter(prefix="/api", tags=["User & Mood"])


@router.post("/user-mood")
async def getUserMood(user_mood: User_Mood) -> dict[str, str | int]:
    return {"energy_level": user_mood.energy_level, "age": user_mood.age}
