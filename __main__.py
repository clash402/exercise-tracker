import requests as req
from datetime import datetime
from decouple import config


# PROPERTIES
NUTRITION_IX_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"
NUTRITION_IX_APP_ID = config("NUTRITION_IX_APP_ID")
NUTRITION_IX_KEY = config("NUTRITION_IX_KEY")

SHEETY_ENDPOINT = config("SHEETY_ENDPOINT")
SHEETY_TOKEN = config("SHEETY_TOKEN")

GENDER = config("GENDER")
WEIGHT = config("WEIGHT")
HEIGHT = config("HEIGHT")
AGE = config("AGE")


# NUTRITION IX
def get_exercise_from_user():
    return input("Tell me which exercises you did: ")


def get_nutrition_ix_data(exercise):
    nutrition_ix_params = {"query": exercise, "gender": GENDER, "weight_kg": WEIGHT,
                           "height_cm": HEIGHT, "age": AGE}
    nutrition_ix_headers = {"x-app-id": NUTRITION_IX_APP_ID, "x-app-key": NUTRITION_IX_KEY}
    res = req.post(NUTRITION_IX_ENDPOINT, json=nutrition_ix_params, headers=nutrition_ix_headers)
    return res.json()


# SHEETY
def post_to_sheety(data):
    today_date = datetime.now().strftime("%d/%m/%Y")
    now_time = datetime.now().strftime("%X")
    sheety_inputs = {}

    for exercise in data["exercises"]:
        sheety_inputs = {
            "workout": {
                "date": today_date,
                "time": now_time,
                "exercise": exercise["name"].title(),
                "duration": exercise["duration_min"],
                "calories": exercise["nf_calories"]
            }
        }

    sheety_headers = {"Authorization": f"Bearer {SHEETY_TOKEN}"}
    req.post(SHEETY_ENDPOINT, json=sheety_inputs, headers=sheety_headers)


# MAIN
if __name__ == "__main__":
    exercise_text = get_exercise_from_user()
    nutrition_ix_data = get_nutrition_ix_data(exercise_text)

    post_to_sheety(nutrition_ix_data)
