import requests
import pandas as pd

URL = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"

res = requests.get(URL, timeout=10)
res.raise_for_status()  

data = res.json()

print("總站點數 =", len(data))
print("前 3 筆站名：", [d["sna"] for d in data[:3]])

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

df = pd.DataFrame(data)
df.to_csv("youbike_raw.csv", index=False, encoding="utf-8-sig")
print("\nyoubike_raw.csv 已經存檔完成")

top10 = (
    df[["sna", "available_rent_bikes"]]
    .sort_values("available_rent_bikes", ascending=True)
    .head(10)
)
result = top10.to_dict(orient="records")
print("\n可借車最少的前 10 站：")
for item in result:
    print(f"站名：{item['sna']}\t可借車：{item['available_rent_bikes']}")
