import requests
import os
import json
from datetime import datetime
from openai import OpenAI


def convert_date(x):
    dt_object = datetime.fromtimestamp(x)
    date = dt_object.date()
    return date


def convert_time(x):
    dt_object = datetime.fromtimestamp(x)
    time = dt_object.time()
    return time


def weather():

    lat = "40.75"
    lon = "-73.88"

    key = os.getenv("weather_api_key")
    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,alerts&units=imperial&appid={key}"

    response_raw = requests.get(url)
    response_json = response_raw.json()
    today_json = response_json["daily"][0]
    today_utc = today_json["dt"]
    date = convert_date(today_utc)

    summary = today_json["summary"]

    sunrise_utc = today_json["sunrise"]
    sunrise = convert_time(sunrise_utc)

    sunset_utc = today_json["sunset"]
    sunset = convert_time(sunset_utc)

    humidity = today_json["humidity"]

    day_temp = today_json["temp"]["day"]
    min_temp = today_json["temp"]["min"]
    max_temp = today_json["temp"]["max"]

    today_json = json.dumps(today_json, indent=4)
    return date, summary, sunrise, sunset, humidity, day_temp, min_temp, max_temp


def bot_ai(date, summary, sunrise, sunset, humidity, day_temp, min_temp, max_temp):

    client = OpenAI()

    personality = """
    You are an AI bot named "Tempo". You are courteous yet direct. You are providing a morning update about today"s weather for me, Ken.
    """

    prompt = f"""
    In three setences and no more than 60 words, give me a good morning and an update on the weather using the following: \n\nDate: {date}\nSummary: {summary}\nSunrise: {sunrise}\nSunset: {sunset}\nHumidity: {humidity}\nDay Temp: {day_temp}\nMin Temp: {min_temp}\nMax Temp: {max_temp}. In one sentence, sign the message.
    """

    subject_init = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": personality},
            {"role": "user", "content": prompt}
            ]
    )
    response = subject_init.choices[0].message.content
    return response


if __name__ == "__main__":

    date, summary, sunrise, sunset, humidity, day_temp, min_temp, max_temp = weather()
    ai = bot_ai(date, summary, sunrise, sunset, humidity, day_temp, min_temp, max_temp)
    print(ai)
