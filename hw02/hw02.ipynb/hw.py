import csv

with open("orders.csv", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

print(list(rows[0].keys()))

def to_num(s):
    s = str(s).strip().replace(" ", "").replace("\xa0", "").replace(",", ".")
    if s == "":
        return None
    try:
        return float(s)
    except ValueError:
        return None

cities = {
    "almaty": "Алматы", "алматы": "Алматы",
    "astana": "Астана", "астана": "Астана",
    "shymkent": "Шымкент", "шымкент": "Шымкент",
    "karaganda": "Караганда", "караганда": "Караганда",
    "aktobe": "Актобе", "актобе": "Актобе",
    "atyrau": "Атырау", "атырау": "Атырау",
}

def clean_city(s):
    s = s.strip().lower()
    return cities.get(s, s.capitalize())

print(set(clean_city(r["city"]) for r in rows))

cat_count = {}
for r in rows:
    cat = r["category"]
    cat_count[cat] = cat_count.get(cat, 0) + 1

for cat, n in sorted(cat_count.items(), key=lambda x: x[1], reverse=True):
    print(cat, n)

rev = {}
cnt = {}
for r in rows:
    if r["status"] != "paid":
        continue
    amount = to_num(r["amount"])
    if amount is None:
        continue
    cat = r["category"]
    rev[cat] = rev.get(cat, 0) + amount
    cnt[cat] = cnt.get(cat, 0) + 1

print(f"{'Категория':<20}{'Заказов':>10}{'Выручка':>15}{'Ср. чек':>12}")
for cat in rev:
    print(f"{cat:<20}{cnt[cat]:>10}{rev[cat]:>15,.0f}{rev[cat] / cnt[cat]:>12,.0f}")

months = {}
for r in rows:
    m = r["order_date"][:7]
    months[m] = months.get(m, 0) + 1

for m in sorted(months):
    print(m, months[m])