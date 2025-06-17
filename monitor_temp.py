import requests

# ✅ ThingSpeak setup
CHANNEL_ID = '2934951'
READ_API_KEY = 'E7RQKIMK7PAU93KQ'

# ✅ Telegram Bot setup
BOT_TOKEN = '8070646137:AAFyRkOYHkRLiUmszK5qHwt3H7wKNpR5Llo'
CHAT_ID = '1065018397'

# ✅ Alert threshold
TEMP_THRESHOLD = 0.1

def get_latest_temps():
    url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?api_key={READ_API_KEY}&results=2"
    response = requests.get(url)
    data = response.json()
    feeds = data.get('feeds', [])
    if len(feeds) < 2:
        raise ValueError("Not enough data to compare.")
    temp1 = float(feeds[0]['field1'])
    temp2 = float(feeds[1]['field1'])
    return temp2, temp1

def send_telegram_alert(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': msg}
    r = requests.post(url, data=payload)
    if r.status_code == 200:
        print("✅ Telegram alert sent.")
    else:
        print("❌ Telegram error:", r.text)

def check_temperature():
    try:
        current, previous = get_latest_temps()
        diff = abs(current - previous)
        print(f"{previous}°C ➡️ {current}°C (Δ = {diff:.2f}°C)")
        if diff >= TEMP_THRESHOLD:
            msg = f"⚠️ Temp Alert:\nFrom {previous:.2f}°C ➡️ {current:.2f}°C\nChange: {diff:.2f}°C"
            send_telegram_alert(msg)
        else:
            print("Stable temp.")
    except Exception as e:
        print("❌ Error:", e)

# 🔁 Run once per minute via Render
check_temperature()
