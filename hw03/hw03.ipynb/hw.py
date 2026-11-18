import csv
import os
import numpy as np

try:
    here = os.path.dirname(os.path.abspath(__file__))
except NameError:
    here = os.getcwd()
path = None
for p in [os.path.join(os.getcwd(), "orders.csv"),
          os.path.join(here, "orders.csv"),
          os.path.join(os.path.dirname(here), "orders.csv")]:
    if os.path.exists(p):
        path = p
        break
if path is None:
    raise SystemExit("Не нашёл orders.csv. Положите его рядом с файлом.")

CITY = {"алматы": "Алматы", "almaty": "Алматы", "астана": "Астана", "astana": "Астана",
        "шымкент": "Шымкент", "shymkent": "Шымкент", "караганда": "Караганда",
        "актобе": "Актобе", "атырау": "Атырау",
        "karaganda": "Караганда", "aktobe": "Актобе", "atyrau": "Атырау"}

with open(path, encoding="utf-8-sig") as f:
    rows = list(csv.DictReader(f))

amount = np.array([float(r["amount"].replace(" ", "")) for r in rows])
paid = np.array([r["status"] == "оплачен" for r in rows])
days = np.array([float(r["delivery_days"]) if r["delivery_days"] else np.nan for r in rows])
city = np.array([CITY.get(r["city"].strip().lower(), r["city"].strip()) for r in rows])
cust = np.array([r["customer_id"] for r in rows])

i = amount.argmax()
print("1. Позиция:", i)
print("   Сумма:", amount[i], "| клиент:", cust[i], "| город:", city[i])

print("2. Оплачено:", round(amount[paid].sum()))
print("   Не оплачено:", round(amount[~paid].sum()))

mask = city == "Шымкент"
print("3. Заказов в Шымкенте:", mask.sum())
print("   Доля от всех:", round(mask.mean() * 100, 1), "%")