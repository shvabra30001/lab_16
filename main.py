import os
import json
from datetime import datetime
import requests
import pandas as pd

print("Задание 1")
host = "jsonplaceholder." + "typicode.com"
url = f"https://{host}/users"
response = requests.get(url)
print("Статус-код:", response.status_code)

if response.status_code == 200:
    print("Задание 2")
    data = response.json()
    print("Всего пользователей:", len(data))

    for user in data:
        print(user["name"], "-", user["email"])

    first_user = data[0]
    print(first_user["address"]["city"])

    print("Задание 3")
    df = pd.DataFrame(data)
    cols = list(("id", "name", "username", "email", "phone", "website"))
    df = df[cols]
    print(df.head())

    print("Задание 4")
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/users.csv", index=False, encoding="utf-8")

    with open("data/users.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("Файлы сохранены:", os.listdir("data"))

    print("Задание 5")
    dirty = [dict(u) for u in data]
    u0 = dirty[0]
    u1 = dirty[1]
    u0["email"] = None
    dirty.append(u1)

    df_dirty = pd.DataFrame(dirty)
    df_dirty = df_dirty[list(("id", "name", "email"))]

    print("Пропуски по колонкам:")
    print(df_dirty.isnull().sum())
    print("Найдено дубликатов:", df_dirty.duplicated().sum())
else:
    print("Запрос не удался, код:", response.status_code)

print("Задание 6")
def fetch_and_backup(api_url, folder="data"):
    resp = requests.get(api_url)
    if resp.status_code != 200:
        print("Запрос не удался, код:", resp.status_code)
        return None

    res_data = resp.json()
    stamp = datetime.now().strftime("%Y-%m-%d")
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"users_{stamp}.json")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(res_data, f, ensure_ascii=False, indent=2)

    print("Бэкап сохранён:", path)
    return pd.DataFrame(res_data)

df_backup = fetch_and_backup(url)
