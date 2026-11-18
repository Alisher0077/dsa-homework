cities  = [" almaty", "Astana", "SHYMKENT", "Almaty ", "karaganda", "astana", "Almaty", "Aktobe", "Astana", "shymkent", "Almaty", "Atyrau"]
amounts = ["15990", "4500", "32000", "870", "12500", "56000", "2300", "9900", "18000", "7400", "41000", "3300"]
paid    = [True, True, False, True, True, False, True, True, True, False, True, True]
days    = ["пн", "пн", "вт", "вт", "ср", "ср", "чт", "пт", "пт", "сб", "сб", "вс"]


cities_clean = []
for c in cities:
    cities_clean.append(c.strip().capitalize())
print(cities_clean)

amounts_int = []
for a in amounts:
    amounts_int.append(int(a))
print(amounts_int)

count = len(amounts_int)
total = sum(amounts_int)
avg = round(total / count)
print("Всего заказов:", count)
print("Общая сумма:", total)
print("Средний чек:", avg)

unpaid_count = 0
unpaid_sum = 0
for a, p in zip(amounts_int, paid):
    if not p:
        unpaid_count += 1
        unpaid_sum += a
print("Не оплачено заказов:", unpaid_count)
print("На сумму:", unpaid_sum)

for city, amount, p in zip(cities_clean, amounts_int, paid):
    status = "оплачен" if p else "не оплачен"
    print(f"{city} | {amount} | {status}")