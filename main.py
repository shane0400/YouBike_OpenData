import requests
import pandas as pd

# 1. YouBike API URL
URL = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"

# 2. 發送 GET 請求，設定 timeout 10 秒
res = requests.get(URL, timeout=10)
res.raise_for_status()  # 如果 HTTP 狀態不是 200，就會拋例外，方便我們 debug

# 3. 解析回傳的 JSON，放到 data（List of dict）
data = res.json()

# 4. 印出「總站點數」和「前 3 筆站名」
print("總站點數 =", len(data))
print("前 3 筆站名：", [d["sna"] for d in data[:3]])

# 5. 篩選「站名、可借車、可還車」欄位，並印出前 5 筆做示範
sample = [
    {
        "站名": d["sna"],
        "可借車": d["available_rent_bikes"],
        "可還車": d["available_return_bikes"]
    }
    for d in data[:5]
]
print("\n前 5 筆範例：")
for row in sample:
    print(row)

# 6. 將整份 JSON 轉換成 DataFrame，並存為 CSV
df = pd.DataFrame(data)
df.to_csv("youbike_raw.csv", index=False, encoding="utf-8-sig")
print("\nyoubike_raw.csv 已經存檔完成")

# 7. 簡易分析：找「可借車最少的前 10 站」
top10 = (
    df[["sna", "available_rent_bikes"]]
    .sort_values("available_rent_bikes", ascending=True)
    .head(10)
)
result = top10.to_dict(orient="records")
print("\n可借車最少的前 10 站：")
for item in result:
    print(f"站名：{item['sna']}\t可借車：{item['available_rent_bikes']}")
