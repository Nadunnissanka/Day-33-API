# import library
from datetime import datetime
import requests
import smtplib
import time

MY_LAT = 6.847278
MY_LONG = 79.926605
MY_EMAIL = "nadunnissankatest@gmail.com"
MY_PASSWORD = "nadun123"


def is_iss_overhead():
    # get request to the API End point
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    # raise an exception if response code is not 200
    response.raise_for_status()
    # getting actual data in JSON format
    data = response.json()
    # getting ISS Longitude
    iss_longitude = float(data["iss_position"]["longitude"])
    iss_latitude = float(data["iss_position"]["latitude"])
    if MY_LONG - 5 <= iss_longitude <= MY_LONG + 5 and MY_LAT - 5 <= iss_latitude <= MY_LAT + 5:
        return True


def is_night():
    # execute the code every 60 seconds
    time.sleep(60)
    # Sunrise Sunset API
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0
    }
    sunrise_sunset_response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    sunrise_sunset_response.raise_for_status()
    sunrise_sunset_data = sunrise_sunset_response.json()
    sunrise_time = int(sunrise_sunset_data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset_time = int(sunrise_sunset_data["results"]["sunset"].split("T")[1].split(":")[0])
    current_time = datetime.now().hour
    if current_time >= sunset_time or current_time <= sunrise_time:
        return True


while True:
    if is_iss_overhead() and is_night():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs="nadun.2018094@iit.ac.lk",
                msg=f"Subject:International Space Station is Above You!\n\nInternational Space Station can been seen now from your location! Look up quick!!"
            )
