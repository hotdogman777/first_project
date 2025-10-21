# geocode_rainfall.py
# pip install geopy pandas

from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import time
import json
import csv
import os
import re

# 1) 너가 준 "도시명, 강수량" 원본 리스트 (그대로 붙여넣음)
raw = [
    "울릉도", 1541,
    "울진", 1198.3,
    "안동", 1002.4,
    "상주", 1157.6,
    "포항", 1172.5,
    "창원", 1436.2,
    "통영", 1664.5,
    "진주", 1537.1,
    "김해시", 1375.2,
    "양산시", 1504,
    "의령군", 1355,
    "함양군", 1325.1,
    "봉화", 1089.2,
    "영주", 1267.5,
    "문경", 1273,
    "청송군", 967.2,
    "영덕", 1113.4,
    "의성", 920.5,
    "구미", 1132,
    "영천", 1076.1,
    "경주시", 1121.2,
    "거창", 1240.7,
    "합천", 1394.9,
    "밀양", 1214.5,
    "산청", 1592.8,
    "거제", 1999.7,
    "남해", 2002.3,
    "영양", 1009.1,
    "성주", 1145.8,
    "고령", 1266.7,
    "청도", 1229,
    "예천", 978.2,
    "김천", 1084.2,
    "칠곡", 1089,
    "경산", 1114.1,
    "삼천포", 1462.6,
    "고성", 1560.7,
    "창녕", 1187,
    "함안", 1322.3,
    "하동", 1770.8,
    "군산", 1265.4,
    "목포", 1193.9,
    "여수", 1499.9,
    "흑산도", 1155.4,
    "완도", 1508.6,
    "고창", 1225.5,
    "부안", 1213.6,
    "임실", 1347.9,
    "정읍", 1292.9,
    "남원", 1339.6,
    "장수", 1529.9,
    "영광군", 1300.1,
    "순창군", 1436.7,
    "강진군", 1430.7,
    "장흥", 1433,
    "해남", 1269.3,
    "고흥", 1533.7,
    "진도군", 1392.8,
    "무안", 1244.9,
    "무주", 1116.4,
    "익산", 1169.7,
    "진안", 1381.2,
    "담양", 1381.4,
    "구례", 1326.6,
    "나주", 1404.5,
    "순천시", 1549.9,
    "광양읍", 1509.3,
    "거문도", 1443.2,
    "장성", 1374.5,
    "영암", 1247.1,
    "보성", 1644.6,
    "완주", 1339.3,
    "김제", 1179.5,
    "화순", 1372.1,
    "함평", 1401.5,
    "곡성", 1402.2,
    "압해도", 1203,
    "전주", 1280.6,
    "충주", 1168,
    "서산", 1156.5,
    "청주", 1194.1,
    "추풍령", 1184.5,
    "제천", 1275,
    "보은", 1320.3,
    "천안", 1178.8,
    "보령", 1135.4,
    "부여", 1310.5,
    "금산", 1267,
    "단양", 1059.8,
    "진천", 1227.4,
    "괴산", 1208.7,
    "옥천", 1187.2,
    "홍북", 1229.6,
    "공주", 1197.4,
    "서천", 1236.9,
    "논산", 1221.1,
    "당진", 1063.1,
    "청양", 1310.8,
    "음성", 1121.9,
    "증평", 1163.7,
    "태안", 1130.3,
    "예산", 1136,
    "아산", 1083.9,
    "계룡", 1383.1,
    "속초", 1397.7,
    "철원", 1308,
    "대관령", 1329.1,
    "춘천", 1295.4,
    "강릉", 1391.3,
    "동해", 1237.8,
    "원주", 1203,
    "영월", 1174.8,
    "인제", 1141.2,
    "홍천", 1153,
    "태백", 1273.9,
    "정선군", 1126.6,
    "간성", 1387.7,
    "평창", 1166.2,
    "횡성", 1175.2,
    "화천", 1176.7,
    "양구", 1145.1,
    "진부령", 1820.5,
    "양양", 1363.1,
    "사북", 1257.1,
    "삼척", 1224.6,
    "동두천", 1314.5,
    "파주", 1196.3,
    "수원", 1294.1,
    "양평", 1289,
    "이천", 1258.7,
    "부천", 1135.4,
    "안양", 1253.9,
    "광명", 1206.7,
    "군포", 1271.8,
    "김포", 1068.4,
    "하남", 944.8,
    "의왕", 1306.7,
    "포천", 1272.4,
    "가평조종", 1440.1,
    "안성", 1181.2,
    "의정부", 1331.9,
    "고양", 1179,
    "남양주", 1312.5,
    "안산", 1103.3,
    "경기광주", 1362.1,
    "여주", 1129.6,
    "용인", 1268.9,
    "오산", 1171.5,
    "평택", 1106.3,
    "시흥", 1160.4,
    "구리", 1281.1,
    "화성", 1097.5,
    "성남", 1253.3,
    "과천", 1276.2,
    "양주", 1195.3,
    "연천청산", 1232.5,
    "제주", 1520.7,
    "고산", 1218.5,
    "성산", 2156.6,
    "서귀포", 2089.3,
    "세종연서", 1152.8,
    "추자도", 1134.3,
    "성판악", 4529.1,
    "백령도", 749.2,
    "인천", 1102.7,
    "대전", 1291.2,
    "울산", 1278.3,
    "광주", 1347.1,
    "부산", 1614.1,
    "강화", 1144.6,
    "인천연수", 1083.3,
    "금곡", 1072.5,
    "문화", 1308.4,
    "세천", 1248.9,
    "장동", 1248.5,
    "부평", 1142.6,
    "광산", 1319.1,
    "조선대", 1339.6,
    "풍암", 1357.8,
    "군위", 936,
    "달성", 1120.2,
    "서구", 1125.1,
    "대구", 1110.1,
    "울기", 1272.1,
    "영도", 1544.9,
    "가덕도", 1405.4,
    "기장", 1464.2,
    "간절곶", 1410.9,
    "해운대", 1582.7,
    "부산진", 1613.9,
    "동래", 1465.8,
    "북구", 1349.8,
    "부산남구", 1613.8,
    "정자", 1257.1,
]

# 2) (중요) 모호한 지명 → 시/도 힌트 보정 맵
#    예: '정자'는 전국에 많아서 '정자, 대전' 식으로 의도한 지역을 지정
HINTS = {
    "정자": "정자동, 대전",
    "세천": "세천동, 대전",
    "문화": "문화동, 대전",
    "장동": "장동, 대전",
    "금곡": "금곡동, 대전",      # 필요 시 수정
    "서구": "서구, 대전",
    "북구": "북구, 부산",
    "부산남구": "남구, 부산",
    "부산진": "부산진구, 부산",
    "해운대": "해운대구, 부산",
    "동래": "동래구, 부산",
    "영도": "영도구, 부산",
    "울기": "울기등대, 동구, 울산광역시",
    "간절곶": "간절곶, 울산",
    "가덕도": "가덕도, 부산",
    "삼천포": "사천시 삼천포, 경남",
    "광양읍": "광양읍, 전남",
    "순천시": "순천시, 전남",
    "압해도": "압해도, 전남",
    "거문도": "거문도, 전남",
    "흑산도": "흑산도, 전남",
    "성산": "성산읍, 제주",
    "성판악": "성판악, 제주",
    "고산": "고산리, 제주",
    "세종연서": "연서면, 세종",
    "연천청산": "청산면, 연천군, 경기",
    "가평조종": "조종면, 가평군, 경기",
    "인천연수": "연수구, 인천",
    "부평": "부평구, 인천",
    "광산": "광산구, 광주",
    "조선대": "조선대학교, 광주",
    "풍암": "풍암동, 광주",
    "서구(중복방지)": "서구, 광주",
    "홍북": "홍북읍, 홍성군, 충청남도",  # 필요 시 키 변경
}

# 3) 지오코더 설정 (OpenStreetMap Nominatim)
geolocator = Nominatim(user_agent="rainfall_geocoder_kr")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1, max_retries=3, error_wait_seconds=2.0)


def to_pairs(lst):
    # ["이름", 값, "이름", 값, ...] -> [("이름", 값), ...]
    return list(zip(lst[0::2], lst[1::2]))


pairs = to_pairs(raw)

# 4) 캐시 (다시 실행 시 API 호출 최소화)
CACHE_FILE = "geocode_cache_kr.json"
cache = {}
if os.path.exists(CACHE_FILE):
    try:
        cache = json.load(open(CACHE_FILE, "r", encoding="utf-8"))
    except Exception:
        cache = {}


def lookup_place(name: str):
    q = HINTS.get(name, name) + ", 대한민국"
    if q in cache:
        if rain is not None and "rain_mm" not in cache[q]:
            cache[q]["rain_mm"] = float(rain)
        return cache[q]

    loc = geocode(q, language="ko")
    if loc:
        cache[q] = {
            "lat": loc.latitude,
            "lon": loc.longitude,
            "raw_name": name,
            "query": q,
            "rain_mm": float(rain) if rain is not None else None
        }
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
        return cache[q]
    return None


results = []
unresolved = []

for name, rain in pairs:
    info = lookup_place(name)
    if info is None:
        unresolved.append((name, rain))
    else:
        results.append([name, info["lat"], info["lon"], float(rain)])

# 5) 안 잡히는 경우, 간단한 보정 시도 (군/군청/읍/면/도서 등)


def heuristic_fix(name):
    # 이름 패턴별 간단 보정
    if name.endswith("군"):
        return name + "청, 대한민국"
    if name.endswith("시"):
        return name + "청, 대한민국"
    if name.endswith("읍") or name.endswith("면") or name.endswith("동"):
        return name + ", 대한민국"
    # 섬/산/고개 등:
    special = {
        "진부령": "진부령, 강원",
    }
    return special.get(name, name + ", 대한민국")


for name, rain in unresolved[:]:
    q = heuristic_fix(name)
    if q in cache:
        info = cache[q]
        results.append([name, info["lat"], info["lon"], float(rain)])
        unresolved.remove((name, rain))
        continue
    loc = geocode(q, language="ko")
    if loc:
        cache[q] = {"lat": loc.latitude, "lon": loc.longitude, "raw_name": name, "query": q}
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
        results.append([name, loc.latitude, loc.longitude, float(rain)])
        unresolved.remove((name, rain))

# 6) 결과 저장
results.sort(key=lambda x: x[0])  # 이름순
with open("rainfall_with_coords.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["name", "lat", "lon", "rain_mm"])
    for row in results:
        w.writerow(row)

with open("rainfall_with_coords.py", "w", encoding="utf-8") as f:
    f.write("rainfall_data = [\n")
    for name, lat, lon, rain in results:
        f.write(f'    ["{name}", {lat:.6f}, {lon:.6f}, {rain}],\n')
    f.write("]\n")

# 7) 로그 출력
print(f"총 {len(pairs)}개 중 좌표 매칭: {len(results)}개")
if unresolved:
    print("다음 지점은 모호/실패하여 수동확인 필요:")
    for n, r in unresolved:
        print(" -", n, r)
else:
    print("모든 지점 좌표 매칭 성공!")
