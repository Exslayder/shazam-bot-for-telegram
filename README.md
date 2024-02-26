## This is a telegram bot that receives voice messages. Recognizes the music in it and sends the name of the track and links to Spotify, Soundcloud, YouTube

![Static Badge](https://img.shields.io/badge/python3-telebot-blue?link=https%3A%2F%2Fpypi.org%2Fproject%2FpyTelegramBotAPI%2F)![Static Badge](https://img.shields.io/badge/python3-yt_dlp-red?link=https%3A%2F%2Fpypi.org%2Fproject%2Fyt-dlp%2F)

## How start

1.  Clone the repository:

    ```bash
    git clone https://github.com/Exslayder/shazam-bot-for-telegram.git
    ```

2.  Install modules:

    ```bash
    pip install asyncio
    pip install bytesbufio
    pip install SpeechRecognition
    pip install pydub
    pip install shazamio
    pip install pycopy-urllib.parse
    pip install pyTelegramBotAPI
    pip install requests
    ```

3.  Create your bot using [**@BotFather**](https://t.me/BotFather) in telegram:

    3.1 Replace the word **TOKEN** with the token of your created bot:

    ```bash
    bot = telebot.TeleBot("TOKEN")
    ```

    3.2 Find out your ID using [**@userinfobot**](https://t.me/userinfobot) and replace the phrase **YOUR_ID**:

    ```bash
    allowed_user_id = YOUR_ID
    ```

    > [**@BotFather**](https://t.me/BotFather) and [**@userinfobot**](https://t.me/userinfobot) are the names of the bots in telegram.

    > **This ID** will help you to use the bot on your Telegram account only. This feature is available to prevent other users from using the bot.

    > How to create a bot and get **TOKEN**:![How to create a bot and get TOKEN](https://assets-global.website-files.com/5d4bc52e7ec3666956bd3bf1/5ebd37e590f1424c4abfa1c2_botfather.jpg)

## Launch

1. Go to the project directory:

   ```bash
   cd shazam-bot-for-telegram
   ```

2. Run the main script:

   ```bash
   python main.py
   ```

3. Send a voice message to your bot and get the result.
