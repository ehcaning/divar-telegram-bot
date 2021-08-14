import requests
import json


URL = "https://api.divar.ir/v8/web-search/<SEARCH-CONDITIONS-HERE>"
TOKENS = list()
BOT_TOKEN = '<BOT-TOKEN-HERE>'
BOT_CHATID = '<CHAT-ID-HERE>'


def get_data():
    response = requests.get(URL)
    return response


def parse_data(data):
    return json.loads(data.text)


def get_houses_list(data):
    return data['web_widgets']['post_list']


def extract_each_house(house):
    data = house['data']

    return {
        'title': data['title'],
        'description': data['description'],
        'district': data['district'],
        'token': data['token'],
    }


def send_telegram_message(house):
    url = 'https://api.telegram.org/bot' + BOT_TOKEN + '/sendMessage'
    text = f"<b>{house['title']}</b>"+"\n"
    text += f"<i>{house['district']}</i>"+"\n"
    text += f"{house['description']}"+"\n\n"
    text += f"https://divar.ir/v/a/{house['token']}"

    body = {
        'chat_id': BOT_CHATID,
        'parse_mode': 'HTML',
        'text': text
    }

    requests.post(url, data=body)


def load_tokens():
    with open("tokens.json", "r") as content:
        if content == "":
            return []
        return json.load(content)


def save_tokns(tokens):
    with open("tokens.json", "w") as outfile:
        json.dump(tokens, outfile)


if __name__ == "__main__":
    tokens = load_tokens()

    data = get_data()
    data = parse_data(data)
    data = get_houses_list(data)

    for house in data:
        house_data = extract_each_house(house)
        if house_data is None:
            continue
        if house_data['token'] in tokens:
            continue

        tokens.append(house_data['token'])
        send_telegram_message(house_data)

    save_tokns(tokens)
