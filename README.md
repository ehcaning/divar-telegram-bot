# Divar Telegram Bot

 A simple crawler and notifier of divar.ir advertisements, based on pre-defined conditions.

## Introduction

This telegram bot notifies you whenever a new ad appears in the specified topic on [Divar](https://divar.ir), an Iranian Persian classified ads and E-commerce app.

## Usage

### Pre-requisites

1. Open `@BotFather` in Telegram, create a new bot, and note its token (Or use an existing bot token) to use in the `.env` file later.
2. Send a message to `@getidsbot` and the response should be something like this:

   ``` text
   👤 You
   ├ id: 00000000
   ├ is_bot: false
   ├ first_name: Ehsan
   ├ last_name: Seyedi
   ├ username: _ (https://t.me/_)
   ├ language_code: en (-)
   └ created: ~ 2/2014 (?) (https://t.me/getidsbot?start=idhelp)
   ```

   Note the `id` to use in the `.env` file later.
3. Open your bot (from step 1) and press **Start** (So the bot can send messages to your account chat).
4. Visit the [Divar](https://divar.ir), select your city, and go to the desired category. Choose some search conditions like this:
   ![Divar Search](img/search.png)
   The web browser's URL should be something like this:

   ``` url
   https://divar.ir/s/tehran/rent-residential/abshar?size=65-120
   ```

   Note everything after `https://divar.ir/s/`, in this case, it will be `tehran/rent-residential/abshar?size=65-120`, to use in the `.env` file later like this:

   ``` shell
   SEARCH_CONDITIONS = "tehran/rent-residential/abshar?size=65-120"
   ```

### Local

``` shell
git clone https://github.com/debMan/divar-telegram-bot.git 
cd divar-telegram-bot
cp .env.sample .env
# edit .env file with datas from Pre-requisites step
editor .env
echo '[]' > tokens.json
pip install -r requirements.txt
./main.py
```

### Docker

``` shell
git clone https://github.com/debMan/divar-telegram-bot.git 
cd divar-telegram-bot
cp .env.sample .env
# edit .env file with datas from Pre-requisites step
editor .env
echo '[]' > tokens.json
docker compose up -d
```

### Development

To run the crawler in development mode, simply follow the [Local](#Local) or [Docker](#Local) instructions with an uncommented `build: .` line in the [`docker-compose.yml`](docker-compose.yml) file, then:

``` shell
docker compose up --build 
```

## Final Result

![Divar Search](img/preview.png)
