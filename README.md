# Divar Telegram Bot

1- Open `@BotFather` in Telegram.
2- Create a new bot and copy bot token. (Or use existing bot and copy bot token)
```python
BOT_TOKEN = '<BOT-TOKEN-HERE>'
```
3- Send a message to `@getidsbot` and response should be something like this:
```text
👤 You
 ├ id: 00000000
 ├ is_bot: false
 ├ first_name: Ehsan
 ├ last_name: Seyedi
 ├ username: _ (https://t.me/_)
 ├ language_code: en (-)
 └ created: ~ 2/2014 (?) (https://t.me/getidsbot?start=idhelp)
```
Copy `id` and paste here:
```python
BOT_CHATID = '<CHAT-ID-HERE>'
```

4- Open your new (or old) bot (from step 2) and press `Start` (So bot can send you messages).

5- Go to https://divar.ir/, select your city and go to desired category. Choose some search conditions like this:

![Divar Search](img/search.png)

Web browser's URL should be something like this:
```url
https://divar.ir/s/mashhad/rent-residential/janbaz?districts=1124%2C442&credit=-100000000&rent=-3000000&size=-90
```
Copy everything after `https://divar.ir/s/`, in this case it will be `mashhad/rent-residential/janbaz?districts=1124%2C442&credit=-100000000&rent=-3000000&size=-90`

And paste this here:

```python
URL = "https://api.divar.ir/v8/web-search/<SEARCH-CONDITIONS-HERE>"
```

6- SSH to your server and make a cronjob to execute this code in which frequency you want.

```bash
crontab -e
```

```crontab
*/2 * * * * cd /root/divar_bot; /usr/bin/python3.8 main.py >> /dev/null 2>&1
```
* In this example, repository is in `/root/divar_bot` directory
* This code will run every 2 minutes, if you need any help visit https://crontab.guru/

## Final Result:
![Telegram Messages](img/preview.png)
