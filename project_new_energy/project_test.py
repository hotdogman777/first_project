import pandas as pd
import glob
import folium
from folium import FeatureGroup

path = r"C:/Users/hhc06/OneDrive/문서/기상데이터"
files = glob.glob(path + "/*.xlsx")

dfs = []

for f in files:
    df = pd.read_excel(f)
    dfs.append(df)

merged_df = pd.concat(dfs, ignore_index=True)
merged_df["일시"] = pd.to_datetime(merged_df["일시"], errors='coerce')
merged_df = merged_df[["지점명", "일시", "일조(hr)", "일사(MJ/m2)", "기온(°C)", "강수량(mm)"]]

merged_df = merged_df.dropna()

merged_df["연도"] = merged_df["일시"].dt.year
print(merged_df)

yearly_avg_df = (
    merged_df
    .groupby(["연도", "지점명"])[["일조(hr)", "일사(MJ/m2)", "기온(°C)", "강수량(mm)"]]
    .mean()
    .reset_index()
)

print(yearly_avg_df)


output_path = r"C:/Users/hhc06/OneDrive/문서/기상데이터_연도별평균.xlsx"
with pd.ExcelWriter(output_path) as writer:
    merged_df.to_excel(writer, sheet_name="전체데이터", index=False)
    yearly_avg_df.to_excel(writer, sheet_name="연도별평균", index=False)

# 위도, 경도 데이터를 추가해야 함 (기상청 주요 지점의 좌표)
location_data = {
    '서울': [37.5665, 126.9780],
    '부산': [35.1796, 129.0756],
    '대전': [36.3504, 127.3845],
    '광주': [35.1595, 126.8526],
    '대구': [35.8714, 128.6014],
    # 필요한 지점 추가
}

# 지도 생성
m = folium.Map(location=[36.5, 127.8], zoom_start=7)

# ==============================
# 1️⃣ 일사량 레이어
# ==============================
solar_layer = FeatureGroup(name="☀️ 일사량")

for i, row in yearly_avg_df.iterrows():
    name = row["지점명"]
    if name in location_data:
        lat, lon = location_data[name]
        value = round(row["일사(MJ/m2)"], 2)
        folium.CircleMarker(
            location=[lat, lon],
            radius=value * 30,
            color="orange",
            fill=True,
            fill_color="orange",
            fill_opacity=0.6,
            popup=f"{name}<br>일사량: {value} MJ/m²"
        ).add_to(solar_layer)

solar_layer.add_to(m)

# ==============================
# 2️⃣ 강우량 레이어
# ==============================
rain_layer = FeatureGroup(name="🌧️ 강우량")

for i, row in yearly_avg_df.iterrows():
    name = row["지점명"]
    if name in location_data:
        lat, lon = location_data[name]
        rain = round(row["강수량(mm)"], 2)

        popup_html = f"""
        <div style="font-size:14px; text-align:center; white-space:nowrap;">
        <b>{name}</b> 🌧️ 강우량: {rain} mm
        </div>
        """

        folium.CircleMarker(
            location=[lat, lon],
            radius=rain * 0.3,  # 강우량은 상대적으로 값이 커서 축소
            color="blue",
            fill=True,
            fill_color="blue",
            fill_opacity=0.5,
            popup=f"{name}<br>강우량: {rain} mm", max_width=250
        ).add_to(rain_layer)

rain_layer.add_to(m)

# ==============================
# 3️⃣ 교집합 (일사↑ + 강우↓)
# ==============================
# 평균 기준보다 일사량은 높고, 강수량은 낮은 지역만 표시

solar_mean = yearly_avg_df["일사(MJ/m2)"].mean()
rain_mean = yearly_avg_df["강수량(mm)"].mean()

combo_layer = FeatureGroup(name="☀️🌧️ 일사↑ + 강우↓ (교집합)")

for i, row in yearly_avg_df.iterrows():
    name = row["지점명"]
    if name in location_data:
        lat, lon = location_data[name]
        solar = row["일사(MJ/m2)"]
        rain = row["강수량(mm)"]
        if solar > solar_mean and rain < rain_mean:
            folium.CircleMarker(
                location=[lat, lon],
                radius=10,
                color="green",
                fill=True,
                fill_color="green",
                fill_opacity=0.8,
                popup=f"{name}<br>일사량: {solar:.2f}<br>강우량: {rain:.2f}"
            ).add_to(combo_layer)

combo_layer.add_to(m)

# ==============================
# ✅ 버튼(레이어 선택 컨트롤) 추가
# ==============================
folium.LayerControl(collapsed=False).add_to(m)

m.save("일사량_강우량_교집합지도.html")
