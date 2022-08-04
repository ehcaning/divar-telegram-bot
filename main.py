import requests
import json
import os
import pathlib
from config import *
import datetime

URL = f"https://api.divar.ir/v8/web-search/{SEARCH_CONDITIONS}"
TOKENS = list()
BOT_TOKEN = f"{BOT_TOKEN}"
BOT_CHATID = f"{BOT_CHATID}"


def get_data(page=None):
    if page:
        api_url = URL + f"&page={page}"
    else:
        api_url = URL
    response = requests.get(api_url)
    return response


def parse_data(data):
    return json.loads(data.text)


def get_houses_list(data):
    return data["web_widgets"]["post_list"]


def extract_each_house(house):
    data = house["data"]

    return {
        "title": data["title"],
        "description": f'{data["top_description_text"]}  {data["middle_description_text"]}',
        "district": data["action"]["payload"]["web_info"]["district_persian"],
        "hasImage": data["image_count"] > 0,
        "token": data["token"],
    }


def send_telegram_message(house):
    url = "https://api.telegram.org/bot" + BOT_TOKEN + "/sendMessage"
    text = f"<b>{house['title']}</b>" + "\n"
    text += f"<i>{house['district']}</i>" + "\n"
    text += f"{house['description']}" + "\n"
    if house["hasImage"]:
        text += f"<i>تصویر : </i>" + "✅" + "\n\n"
    else:
        text += f"<i>تصویر : </i>" + "❌" + "\n\n"
    text += f"https://divar.ir/v/a/{house['token']}"
    body = {"chat_id": BOT_CHATID, "parse_mode": "HTML", "text": text}
    result = requests.post(url, data=body)
    if not result.status_code == 200:
        time.sleep(5)
        send_telegram_message(house)


def load_tokens():
    my_path = str(pathlib.Path(__file__).parent.resolve()) + "//"
    with open(my_path + "tokens.json", "r") as content:
        if content == "":
            return []
        return json.load(content)


def save_tokns(tokens):
    with open("tokens.json", "w") as outfile:
        json.dump(tokens, outfile)


def get_data_page(page=None):
    data = get_data(page)
    data = parse_data(data)
    data = get_houses_list(data)
    data = data[::-1]
    return data


def process_data(data, tokens):
    for house in data:
        house_data = extract_house_data(house)
        if house_data is None:
            continue
        if house_data["token"] in tokens:
            continue

        tokens.append(house_data["token"])
        send_telegram_message(house_data)
        time.sleep(1)
    return tokens


if __name__ == "__main__":
    print(datetime.datetime.now())
    tokens = load_tokens()
    print(len(tokens))
    pages = [2, ""]
    for page in pages:
        data = get_data_page(page)
        tokens = process_data(data, tokens)

    save_tokns(tokens)
