import requests
from datetime import datetime
import os


API_KEY = os.environ["ENV_API_KEY"]
APP_ID = os.environ["ENV_APP_ID"]
GENDER = BIO_SEX #Pretty sure they mean biological sex here.
MY_WEIGHT = WEIGHT_IN_kg
MY_HEIGHT = HEIGHT_IN_CM
MY_AGE = IN_YEARS

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

exercise_params = {
    "query": input("Tell me which exercises you did: ").title(),
    "gender": GENDER,
    "weight_kg": MY_WEIGHT,
    "height_cm": MY_HEIGHT,
    "age": MY_AGE,
}

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

response = requests.post(url=exercise_endpoint, json=exercise_params, headers=headers)
result = response.json()

exercise_done = result["exercises"][0]["user_input"]
exercise_time = result["exercises"][0]["duration_min"]
cal_burnt = result["exercises"][0]["nf_calories"]

print(result["exercises"][0])

# Create row in Sheety:
now = datetime.now()
today_date = now.strftime("%d/%m/%Y")
today_time = now.strftime("%H:%M:%S")

sheety_url = os.environ["ENV_END_SHEETY"]
sheety_headers = {
    "Authorization": F"Basic {os.environ['ENV_AUTH_SHEETY']}"
}
for exercise in result["exercises"]:
    sheety_params = {
        "workout": {
            "date": today_date,
            "time": today_time,
            "exercise": exercise_done,
            "duration": exercise_time,
            "calories": cal_burnt,
        }
    }

    sheety_response = requests.post(url=sheety_url, json=sheety_params, headers=sheety_headers)
    print(sheety_response.text)
