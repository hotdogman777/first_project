import pandas as pd
import glob
import folium
from solar.solar_map import SolarMap
from rain.rain_map import RainMap
from map.combined_map import CombinedMap

# ============================
# 데이터 로드 및 가공
# ============================
path = r"C:/Users/hhc06/OneDrive/문서/기상데이터"
files = glob.glob(path + "/*.xlsx")

dfs = [pd.read_excel(f) for f in files]
merged_df = pd.concat(dfs, ignore_index=True)

merged_df["일시"] = pd.to_datetime(merged_df["일시"], errors='coerce')
merged_df = merged_df[["지점명", "일시", "일조(hr)", "일사(MJ/m2)", "기온(°C)", "강수량(mm)"]]
merged_df = merged_df.dropna()
merged_df["연도"] = merged_df["일시"].dt.year

yearly_avg_df = (
    merged_df
    .groupby(["연도", "지점명"])[["일조(hr)", "일사(MJ/m2)", "기온(°C)", "강수량(mm)"]]
    .mean()
    .reset_index()
)

# ============================
# 위치 데이터
# ============================
location_data = {
    '서울': [37.5665, 126.9780],
    '부산': [35.1796, 129.0756],
    '대전': [36.3504, 127.3845],
    '광주': [35.1595, 126.8526],
    '대구': [35.8714, 128.6014],
}

# ============================
# 지도 생성 및 레이어 추가
# ============================
m = folium.Map(location=[36.5, 127.8], zoom_start=7)

# 일사량, 강우량, 교집합 레이어 추가
solar_layer = SolarMap(yearly_avg_df, location_data).create_layer()
rain_layer = RainMap(yearly_avg_df, location_data).create_layer()
combo_layer = CombinedMap(yearly_avg_df, location_data).create_layer()

solar_layer.add_to(m)
rain_layer.add_to(m)
combo_layer.add_to(m)

folium.LayerControl(collapsed=False).add_to(m)
m.save("일사량_강우량_교집합지도.html")

print("✅ 지도 생성 완료: 일사량_강우량_교집합지도.html")
