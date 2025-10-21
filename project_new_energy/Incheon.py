import requests
import folium

lat, lon = 37.4563, 126.7052  # 인천 예시

# Open-Meteo 예측 API URL (강수 포함)
url = (
    f"https://api.open-meteo.com/v1/forecast?"
    f"latitude={lat}&longitude={lon}"
    f"&hourly=temperature_2m,precipitation"
    f"&current_weather=true"
)

response = requests.get(url, timeout=5).json()

# 예측 강수 (hourly -> precipitation 리스트 중 첫 값)
hourly = response.get("hourly", {})
precip = hourly.get("precipitation", None)
if precip is not None and len(precip) > 0:
    rain0 = precip[0]
else:
    rain0 = None

# 현재 날씨 온도
current = response.get("current_weather", {})
temp = current.get("temperature", "정보 없음")

print(f"예측 강수: {rain0} mm")
print(f"현재 기온: {temp} °C")

# 지도 표시
m = folium.Map(location=[lat, lon], zoom_start=11)
popup_txt = f"인천 예측 강수: {rain0 if rain0 is not None else '데이터 없음'} mm\n기온: {temp} °C"
folium.Marker([lat, lon], popup=popup_txt).add_to(m)
m.save("incheon_precip.html")
print("✅ incheon_precip.html 생성 완료")
