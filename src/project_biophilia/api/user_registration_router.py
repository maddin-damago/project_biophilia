from fastapi import APIRouter
from pydantic import BaseModel, EmailStr, field_validator
import os
import json
from email_validator import validate_email, EmailNotValidError

# Define the structure of the data you expect from the user


class UserRegistration(BaseModel):
    first_name: str
    last_name: str
    age: int
    email: EmailStr
    password: str

    @field_validator('email')
    @classmethod
    def check_dns(cls, v: str) -> str:
        try:
            validate_email(v, check_deliverability=True)
            return v
        except EmailNotValidError as f:
            raise ValueError(
                f"Die Domain existiert nicht oder ist ungültig: {f}")


router = APIRouter(prefix="/api", tags=["User & Mood"])


@router.post("/user-registration")
async def register(user_registration: UserRegistration) -> dict[str, int | str | UserRegistration | tuple | None]:
    info = userSaveData(user_registration)
    return {"message": "Mood successfully cached in RAM", "Info": info}


def userSaveData(user_registration: UserRegistration):
    try:
        user = user_registration.model_dump()
        datei_name = "src/project_biophilia/api/user_data/user_information.json"
        datei_name_log = "src/project_biophilia/api/user_data/user_login_data.json"

        bestehende_daten = []
        bestehende_daten_log = []
        if os.path.exists(datei_name_log):
            with open(datei_name_log, "r") as f:
                try:
                    bestehende_daten_log = json.load(f)
                except json.JSONDecodeError:
                    bestehende_daten_log = []
        vorhanden = False

        if os.path.exists(datei_name):
            with open(datei_name, "r", encoding="utf-8") as f:
                try:
                    bestehende_daten = json.load(f)
                    for i in bestehende_daten:
                        if i['email'] == user_registration.email:
                            vorhanden = True
                            return "Email existiert schon!"
                except json.JSONDecodeError:
                    bestehende_daten = []

        if not vorhanden:
            bestehende_daten.append({
                "first_name": user["first_name"],
                "last_name": user["last_name"],
                "age": user["age"],
                "email": user["email"]
            })
            bestehende_daten_log.append({
                "email": user["email"],
                "password": user["password"]
            })

            with open(datei_name, "w", encoding="utf-8") as f:
                json.dump(bestehende_daten, f, indent=4)

            with open(datei_name_log, "w", encoding="utf-8") as f:
                json.dump(bestehende_daten_log, f, indent=4)

            angelegt = f"Super, User angelegt: {user_registration}"
            return angelegt

    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
        return f"Interner Fehler beim Speichern: {e}"
