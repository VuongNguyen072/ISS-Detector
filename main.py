from operator import truediv

import requests
from datetime import datetime, timezone
import smtplib
import os

MY_LAT = 10.82302
MY_LONG = 106.62965
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = os.environ.get("MY_EMAIL")
SENDER_PASSWORD = os.environ.get("MY_PASSWORD")
RECEIVER_EMAIL = "nguyenlevuong027@gmail.com"


message = f"""Subject: Hãy nhìn lên bầu trời, có một vì tinh tú tên ISS
From: {SENDER_EMAIL}
To: {RECEIVER_EMAIL}

Như tiêu đề.
"""


def is_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if (MY_LAT-5 <= iss_latitude <= MY_LAT+5) and (MY_LONG-5 <= iss_longitude <= MY_LONG+5):
        return True
    return False

def is_dark():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = int(datetime.now(timezone.utc).hour)

    if (sunset <= time_now) or (sunrise >= time_now):
        return True
    return False


if True:
    try:
        # Kết nối tới server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Bật chế độ bảo mật TLS

        # Đăng nhập
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        # Gửi thư
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message)

        print("Gửi email thành công!")

    except Exception as e:
        print(f"Có lỗi xảy ra: {e}")

    finally:
        # Ngắt kết nối
        server.quit()
else:
    print("not overhead")

