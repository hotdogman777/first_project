import requests
import folium
from dotenv import load_dotenv
import os

load_dotenv()
# ------------------------------------------
#  설정
# ------------------------------------------
API_KEY = os.getenv("OPENWEATHER_KEY")
lat, lon = 35.8250, 128.7424  # 경산

# ------------------------------------------
#  1️⃣ 현재 관측 기반 (/weather)
# ------------------------------------------
url_weather = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=kr"
data_weather = requests.get(url_weather).json()

# "rain" 필드가 없으면 기본값 0
rain_weather = data_weather.get("rain", {}).get("1h", 0)
temp = data_weather["main"]["temp"]
desc = data_weather["weather"][0]["description"]

print(f"[Weather API] 현재 관측값 기준:")
print(f" - 기온: {temp}℃")
print(f" - 날씨: {desc}")
print(f" - 최근 1시간 강수량: {rain_weather}mm\n")

# ------------------------------------------
#  2️⃣ 실시간(분 단위) 예측 (/onecall)
# ------------------------------------------
url_onecall = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=kr"
data_onecall = requests.get(url_onecall).json()

# minutely(분단위) 정보 확인
if "minutely" in data_onecall:
    rain_minutely = data_onecall["minutely"][0].get("precipitation", 0)
    print(f"[OneCall API] 분 단위 실시간 예측 기준:")
    print(f" - 현재 강수량: {rain_minutely}mm (실시간 감지)\n")
else:
    rain_minutely = None
    print("[OneCall API] ⚠️ 이 지역에는 분 단위 데이터(minutely)가 없습니다.\n")

# ------------------------------------------
#  3️⃣ folium 지도 표시
# ------------------------------------------
m = folium.Map(location=[lat, lon], zoom_start=11)

popup_text = f"""
<b>경산 실시간 강우량</b><br>
관측 기준: {rain_weather}mm<br>
예측 기준: {rain_minutely if rain_minutely is not None else '데이터 없음'}mm<br>
기온: {temp}℃<br>
날씨: {desc}
"""
folium.Marker([lat, lon], popup=popup_text).add_to(m)

m.save("realtime_rain_onecall.html")
print("✅ realtime_rain_onecall.html 생성 완료")
