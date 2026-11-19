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
paid   = np.array([r["status"] == "оплачен" for r in rows])
city   = np.array([CITY.get(r["city"].strip().lower(), r["city"].strip()) for r in rows])
cust   = np.array([r["customer_id"] for r in rows])
month  = np.array([r["order_date"][:7] for r in rows])
cat    = np.array([r["category"] for r in rows])
oid    = np.array([r["order_id"] for r in rows])

_, first = np.unique(oid, return_index=True)
keep = np.zeros(len(oid), dtype=bool)
keep[first] = True
clean = keep & (cust != "TEST") & paid
print("строк всего:", len(oid), "| в чистых данных:", clean.sum())

months = np.unique(month)
sep = amount[clean & (month == months[0])].sum()
octo = amount[clean & (month == months[1])].sum()
print("\n1.", months[0], ":", round(sep), "|", months[1], ":", round(octo))
print("   Изменение:", round((octo - sep) / sep * 100, 1), "%")

cats = np.unique(cat)
rev = np.zeros((len(cats), len(months)))
cnt = np.zeros((len(cats), len(months)))
for i, c in enumerate(cats):
    for j, m in enumerate(months):
        mask = clean & (cat == c) & (month == m)
        rev[i, j] = amount[mask].sum()
        cnt[i, j] = mask.sum()

print("\n2. Выручка по категориям:")
print(f"{'':<20}{months[0]:>14}{months[1]:>14}")
for i, c in enumerate(cats):
    print(f"{c:<20}{rev[i, 0]:>14,.0f}{rev[i, 1]:>14,.0f}")

total = rev.sum(axis=1)
print("   Больше всего за два месяца:", cats[total.argmax()], round(total.max()))
change = (rev[:, 1] - rev[:, 0]) / rev[:, 0] * 100
for i, c in enumerate(cats):
    print(f"   {c:<20}{change[i]:>8.1f} %")
print("   Сильнее всех упала:", cats[change.argmin()], round(change.min(), 1), "%")

avg = rev / cnt
print("\n3. Средний чек:")
print(f"{'':<20}{months[0]:>14}{months[1]:>14}")
for i, c in enumerate(cats):
    print(f"{c:<20}{avg[i, 0]:>14,.0f}{avg[i, 1]:>14,.0f}")
print("   Самый высокий в", months[1], ":", cats[avg[:, 1].argmax()], round(avg[:, 1].max()))