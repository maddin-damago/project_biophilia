"""
{
  "fall": "REDUCED_OUTDOOR",
  "condition": "Draußen scheint die Sonne, doch das schöne Wetter passt so gar nicht zu deiner gedrückten Stimmung.",
  "kraeuter_einleitung": "Als leiser Wegweiser zu deiner inneren Natur dürfen dich heute Vogel-Sternmiere und Gundermann begleiten. Nimm dir einen Moment Zeit, um dich mit der lebendigen Kraft dieser Wildkräuter zu verbinden:",
  "kraeuter_details": [
    {
      "trivialName": "Vogel-Sternmiere",
      "botanischerName": "Stellaria media",
      "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/StellariaMedia001.JPG/1280px-StellariaMedia001.JPG",
      "familie": "Caryophyllaceae/ Nelkengewächse",
      "ernte": "ganzjährig",
      "erkennungsmerkmale": [
        "niederliegende oder aufsteigende, auf einer Längslinie behaarte Stängel",
        "kleine weiße Sternblüten",
        "gegenständige Blätter, fiedernervig"
      ],
      "verwechslungsgefahr": ["Acker-Gauchheil (Anagallis arvensis)"],
      "vorkommen": "Gärten, Äcker, Wege und Ufer. Auf sehr Nährstoffreichen Böden, auch im Schatten.",
      "heilwirkung": "Symbolisiert Anpassungsfähigkeit und Resilienz. Entzündungshemmend, schleimlösend und wundheilend. Gilt wegen des hohen Nährstoffgehalts als heimisches Superfood."
    },
    {
      "trivialName": "Gundermann",
      "botanischerName": "Glechoma hederacea",
      "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/79/Glechoma_hederacea_Bluszczyk_kurdybanek_2020-04-24_03.jpg/960px-Glechoma_hederacea_Bluszczyk_kurdybanek_2020-04-24_03.jpg",
      "familie": "Lamiaceae/ Lippenblütler",
      "ernte": "wintergrün",
      "erkennungsmerkmale": [
        "Staude",
        "lilafarbene Blüte mit flacher Oberlippe",
        "Blätter gegenständig, nieren- bis herzförmig, Blattrand gekerbt",
        "kriechender Wuchs",
        "leicht minziger Geschmack"
      ],
      "verwechslungsgefahr": ["keine giftigen Doppelgänger"],
      "vorkommen": "Wiesen, Weiden, Rasenflächen, Auenwälder, Waldränder, Hecken und Böschungen. Auf feucht bis nassen, nährstoffreichen Lehmböden.",
      "heilwirkung": "Fördert langsame Naturerkundung. Seine Hauptwirkung ist entzündungshemmend, schleimlösend und wundheilend. Er wird traditionell bei Erkältungen, Bronchitis und Magen-Darm-Beschwerden sowie zur Unterstützung der Wundheilung eingesetzt."
    }
  ],
  "aktivität": [
    "Geh hinaus an einen besonderen Platz in der Natur, der dir gefällt und an dem du dich wohlfühlst. Einen Ort, an dem du merkst: Hier kann ich mich entspannen. Setze dich nieder und atme zehnmal tief ein und aus.",
    "Nutze die frisch gewonnene Energie, um dich auf den Weg zu machen, die beiden Wildkräuter exakt zu bestimmen und zu sammeln. Nimm dabei nur so viel mit, wie du wirklich verbrauchen wirst. Bereite dir heute einen besonderen Salat zu, den du mit den beiden Wildkräutern verfeinerst, und spüre ganz bewusst, wie die Nährstoffe deinem Körper neue Kraft geben.",
    "Kleiner Tipp: Nimm ruhig etwas mehr von dem Gundermann mit. Dieser lässt sich hervorragend zu einem kleinen Nachtisch verarbeiten, indem du die Blättchen in geschmolzene Schokolade tunkst und fest werden lässt. Durch die feine, minzige Note des Gundermanns kreierst du dir so eine ganz besondere Delikatesse, und dazu lässt Schokolade bekanntlich noch Glücksgefühle frei."
  ],
  "erklaerung": "Wenn die Energie sinkt, regeneriert die vitaminreiche Vogelmiere sanft, während der ausdauernde Gundermann hilft, die restlichen Kräfte im Fluss zu halten, ohne zu überfordern."
}


"""
from functools import reduce
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, HttpUrl
from typing import Literal


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


@router.post("/recommendation")
async def getRecommendation(recommendation: Recommendation_Structure) -> dict[str, str | Recommendation_Structure]:
    global recommendation_data
    recommendation_data = {"data": recommendation}
    return {"message": "Mood successfully cached in RAM"}


def get_latest_recommendation():
    return recommendation_data
