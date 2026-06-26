from functools import reduce
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Literal


# Define the structure of the data you expect from the user
class User_Mood(BaseModel):
    q1: dict[Literal["score", "text"], int | str]
    q2: dict[Literal["score", "text"], int | str]
    q3: dict[Literal["score", "text"], int | str]
    q4: dict[Literal["score", "text"], int | str]
    q5: dict[Literal["score", "text"], int | str]


router = APIRouter(prefix="/api", tags=["User & Mood"])

user_mood_data = None


@router.post("/user-mood")
async def getUserMood(user_mood: User_Mood) -> dict[str, int | str | User_Mood]:
    global user_mood_data
    question_dicts = user_mood.model_dump().values()
    sum = reduce(lambda acc, item: acc + item["score"], question_dicts, 0)
    user_mood_data = {"data": user_mood, "sum": sum}
    return {"message": "Mood successfully cached in RAM", "data": user_mood, "sum": sum}


def get_latest_mood_summary():
    return user_mood_data
