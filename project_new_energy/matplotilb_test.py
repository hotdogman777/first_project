import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

labels = ["Python", "Java", "C++", "JavaScript"]
sizes = [45, 30, 15, 10]

plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)

plt.title("프로그래밍 언어 선호도(파이 차트)")
plt.axis("equal")  # 원이 찌그러지지 않게 설정
plt.show()
