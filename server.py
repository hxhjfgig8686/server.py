import requests
import time
import re
from datetime import datetime
from bs4 import BeautifulSoup
from telegram import Bot
import phonenumbers

# Telegram
TOKEN = "8339174153:AAGbC5O4h66D_Mu6-fghTGThSgGtn4iXjDI"
CHAT_ID = "-1003745034804"

# iVASMS
LOGIN_URL = "https://www.ivasms.com/login"
SMS_URL = "https://www.ivasms.com/portal/live/my_sms"

USERNAME = "asmeralselwi103@gmail.com"
PASSWORD = "Mohammed Saeed 123"

bot = Bot(token=TOKEN)


def get_country(number):
    try:
        parsed = phonenumbers.parse(number)
        country = phonenumbers.region_code_for_number(parsed)
        flag = "".join(chr(127397 + ord(c)) for c in country)
        return f"{flag} {country}"
    except:
        return "🌍 Unknown"


def login(session):
    data = {
        "email": USERNAME,
        "password": PASSWORD
    }

    r = session.post(LOGIN_URL, data=data)

    if r.status_code != 200:
        print("Login failed")
        return False

    print("Login success")
    return True


def fetch_sms(session):
    r = session.get(SMS_URL)

    if r.status_code != 200:
        print("Failed to fetch SMS")
        return None

    return r.text


def parse_sms(html):

    soup = BeautifulSoup(html, "html.parser")

    messages = []

    rows = soup.find_all("tr")

    for row in rows:

        text = row.get_text(" ", strip=True)

        number_match = re.search(r"\+\d{8,15}", text)
        otp_match = re.search(r"\b\d{4,8}\b", text)

        if number_match and otp_match:

            number = number_match.group()
            otp = otp_match.group()

            messages.append({
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "number": number,
                "otp": otp,
                "msg": text
            })

    return messages


def send_telegram(msg):

    country = get_country(msg["number"])

    text = f"""
✨ <b>OTP Received</b>

🕒 Time: {msg['time']}
📞 Number: {msg['number']}
🌍 Country: {country}
🔐 OTP: {msg['otp']}

📝 Message:
{msg['msg']}
"""

    bot.send_message(
        chat_id=CHAT_ID,
        text=text,
        parse_mode="HTML"
    )


def main():

    session = requests.Session()

    if not login(session):
        return

    sent = set()

    while True:

        html = fetch_sms(session)

        if not html:
            time.sleep(10)
            continue

        messages = parse_sms(html)

        for msg in messages:

            if msg["otp"] not in sent:
                send_telegram(msg)
                sent.add(msg["otp"])

        time.sleep(3)


if __name__ == "__main__":
    main()