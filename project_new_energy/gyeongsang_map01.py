import folium

# 직접 코드에 강우량 값을 입력하기 (정적 데이터)

# (도시명, 위도, 경도)
cities = [
    ("경산", 35.8250, 128.7424),
    ("경주", 35.8562, 129.2247),
    ("구미", 36.1195, 128.3446),
    ("김천", 36.1398, 128.1136),
]

# 강우량 데이터 (mm)
rain_data = {
    "경산": 10.2,
    "경주": 5.8,
    "구미": 18.7,
    "김천": 3.4,
}

m = folium.Map(location=[35.8, 128.6], zoom_start=8)

# 강우량에 따라 색상 바꾸기
for name, lat, lon in cities:
    rain = rain_data.get(name, 0)
    color = "red" if rain > 15 else "orange" if rain > 5 else "blue"
    folium.CircleMarker(
        location=[lat, lon],
        radius=10,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7,
        popup=f"<b>{name}</b><br>강우량: {rain}mm",
        tooltip=f"{name}: {rain}mm",
    ).add_to(m)

m.save("rain_map.html")
print("✅ 지도 생성 완료! rain_map.html 열면 강우량 색상 표시됨")
