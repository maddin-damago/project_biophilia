from functools import reduce
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, HttpUrl
from src.project_biophilia.processing.weather_data_processing import weatherDataProcessing
from src.project_biophilia.helpers.aktivitaetsMatching import generiereAktivitaet


# Define the structure of the data you expect from the user
class Herb_Details(BaseModel):
    trivialName: str
    botanischerName: str
    image_url: HttpUrl
    familie: str
    ernte: str
    erkennungsmerkmale: list[str]
    verwechslungsgefahr: list[str]
    vorkommen: str
    heilwirkung: str


class Recommendation_Structure(BaseModel):
    fall: str
    condition: str
    kraeuter_einleitung: str
    kraeuter_details: list[Herb_Details]
    aktivität: list[str]
    erklaerung: str


router = APIRouter(prefix="/api", tags=["Recommendation"])

recommendation_data = None


@router.get("/recommendation")
async def getRecommendation() -> Recommendation_Structure:
    recommendation_key = weatherDataProcessing()
    result = generiereAktivitaet(recommendation_key)
    return result


def get_latest_recommendation():
    return recommendation_data
