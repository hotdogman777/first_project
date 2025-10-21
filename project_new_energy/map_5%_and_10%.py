import folium
import numpy as np
import json

# === 1️⃣ JSON 파일에서 데이터 불러오기 ===
with open("geocode_cache_kr.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# JSON 안의 값을 [이름, 위도, 경도, 강우량] 형태로 변환
cities = []
for key, info in data.items():
    lat = info.get("lat")
    lon = info.get("lon")
    name = info.get("raw_name", key.split(",")[0])
    rain = info.get("rain_mm", None)
    if lat and lon and rain is not None:
        cities.append([name, lat, lon, rain])

print(f"총 {len(cities)}개 지점 로드 완료")

# === 2️⃣ 강우량 값 추출 및 하위 퍼센트 계산 ===
rain_values = [c[3] for c in cities]
cutoff_5 = np.percentile(rain_values, 5)
cutoff_10 = np.percentile(rain_values, 10)

print(f"하위 5% 기준: {cutoff_5:.1f}mm")
print(f"하위 10% 기준: {cutoff_10:.1f}mm")

# === 3️⃣ 지도 생성 ===
m = folium.Map(location=[36.3, 127.8], zoom_start=7, tiles='cartodbpositron')

# === 4️⃣ 색상 조건 분기 ===
for name, lat, lon, rain in cities:
    if rain <= cutoff_5:
        color = 'red'     # 하위 5%
    elif rain <= cutoff_10:
        color = 'blue'    # 하위 10%
    else:
        color = 'gray'    # 나머지

    folium.CircleMarker(
        location=[lat, lon],
        radius=6,
        popup=f"<div style='font-size:14px; line-height:1.4;'><b>{name}</b><br>강우량: {rain} mm</div>",
        tooltip=f"{name} ({rain} mm)",
        color=color,
        fill=True,
        fill_opacity=0.8
    ).add_to(m)

# === 5️⃣ HTML 파일로 저장 ===
m.save("rain_map_from_json.html")
print("✅ 지도 생성 완료 → rain_map_from_json.html 파일을 열어보세요!")
