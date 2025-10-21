import folium
import os
import subprocess

# folium 지도 생성
m = folium.Map(location=[36.472203, 128.621828], zoom_start=15)
file_path = os.path.abspath("map.html")
m.save(file_path)

# ✅ 크롬을 별도 새 창으로 실행
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
subprocess.Popen([chrome_path, file_path])

print("✅ 지도 생성 완료! 크롬 새 창에서 지도 열림.")
