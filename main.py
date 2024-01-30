import datetime
import json
import os
import time

import requests
import telegram
from pydantic import BaseModel
import asyncio


URL = "https://api.divar.ir/v8/web-search/{SEARCH_CONDITIONS}".format(**os.environ)
BOT_TOKEN = "{BOT_TOKEN}".format(**os.environ)
BOT_CHATID = "{BOT_CHATID}".format(**os.environ)
SLEEP_SEC = "{SLEEP_SEC}".format(**os.environ)

proxy_url = None
if os.environ.get("PROXY_URL", ""):
    proxy_url = os.environ.get("PROXY_URL")

TOKENS = list()
# setup telegram bot client
req_proxy = telegram.request.HTTPXRequest(proxy_url=proxy_url)
bot = telegram.Bot(token=BOT_TOKEN, request=req_proxy)


# AD class model
class AD(BaseModel):
    title: str
    price: int
    description: str = ""
    district: str
    images: list[str] = []
    token: str


def get_data(page=None):
    api_url = URL
    if page:
        api_url += f"&page={page}"
    response = requests.get(api_url)
    print("{} - Got response: {}".format(datetime.datetime.now(), response.status_code))
    return response.json()


def get_ads_list(data):
    return data["web_widgets"]["post_list"]


def fetch_ad_data(token: str) -> AD:
    # send request
    data = requests.get(f"https://api.divar.ir/v8/posts-v2/web/{token}").json()
    images = []
    # check post exists
    if not "sections" in data:
        return None

    # get data
    for section in data["sections"]:
        # find title section
        if section["section_name"] == "TITLE":
            title = section["widgets"][0]["data"]["title"]

        # find images section
        if section["section_name"] == "IMAGE":
            images = section["widgets"][0]["data"]["items"]
            images = [img["image"]["url"] for img in images]

        # find description section
        if section["section_name"] == "DESCRIPTION":
            description = section["widgets"][1]["data"]["text"]

    # get district
    district = data["seo"]["web_info"]["district_persian"]
    price = data["webengage"]["price"]

    # create ad object
    ad = AD(
        token=token,
        title=title,
        district=district,
        description=description,
        images=images,
        price=price,
    )

    return ad


async def send_telegram_message(ad: AD):
    text = f"🗄 <b>{ad.title}</b>" + "\n"
    text += f"📌 محل آگهی : <i>{ad.district}</i>" + "\n"
    _price = f"{ad.price:,} تومان" if ad.price else "توافقی"
    text += f"💰 قیمت : {_price}" + "\n\n"
    text += f"📄 توضیحات :\n{ad.description}" + "\n"
    text += f"https://divar.ir/v/a/{ad.token}"

    # send single photo
    if len(ad.images) == 1:
        await bot.send_photo(
            caption=text, photo=ad.images[0], chat_id=BOT_CHATID, parse_mode="HTML"
        )
    # send album
    elif len(ad.images) > 1:
        _media_list = [telegram.InputMediaPhoto(img) for img in ad.images[:10]]
        try:
            await bot.send_media_group(
                caption=text, media=_media_list, chat_id=BOT_CHATID, parse_mode="HTML"
            )
        except telegram.error.BadRequest as e:
            print("Error sending photos :", e)
            return
    else:
        # send just text
        await bot.send_message(text=text, chat_id=BOT_CHATID, parse_mode="HTML")


def load_tokens():
    token_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "tokens.json"
    )
    with open(token_path, "r") as content:
        if content == "":
            return []
        return json.load(content)


def save_tokns(tokens):
    token_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "tokens.json"
    )
    with open(token_path, "w") as outfile:
        json.dump(tokens, outfile)


def get_tokens_page(page=None):
    data = get_data(page)
    data = get_ads_list(data)
    data = data[::-1]
    # get tokens
    data = filter(lambda x: x["widget_type"] == "POST_ROW", data)
    tokens = list(map(lambda x: x["data"]["token"], data))
    return tokens


async def process_data(tokens):
    for token in tokens:
        # get the ad data
        ad = fetch_ad_data(token)
        if not ad:
            continue
        print("AD - {} - {}".format(token, vars(ad)))
        # send message to telegram
        print("sending to telegram token: {}".format(ad.token))
        await send_telegram_message(ad)
        time.sleep(1)


if __name__ == "__main__":
    print("Started at {}.".format(datetime.datetime.now()))
    tokens = load_tokens()
    print("Tokens length: {}".format(len(tokens)))
    pages = [""]
    while True:
        for page in pages:
            # get new tokens list
            tokens_list = get_tokens_page(page)
            # remove repeated tokens
            tokens_list = list(filter(lambda t: not t in tokens, tokens_list))
            tokens = list(set(tokens_list + tokens))
            asyncio.run(process_data(tokens_list))
        # save new tokens
        save_tokns(tokens)
        time.sleep(int(SLEEP_SEC))
