# Шазам со ссылками на ютуб, саундклауд и спотифай, создается временный файлы, потом удаляется
import asyncio
from io import BytesIO
import speech_recognition as sr
from pydub import AudioSegment
from shazamio import Shazam
from urllib.parse import quote
import telebot
import requests
import time

bot = telebot.TeleBot("TOKEN")  # Token from BotFather telegram
allowed_user_id = YOUR_ID  # For personal use in restricted access


def get_spotify_link(track_subtitle, track_title):
    query = f"{track_subtitle} {track_title}"
    return f"https://open.spotify.com/search/{quote(query)}"


def get_soundcloud_link(track_subtitle, track_title):
    query = f"{track_subtitle} {track_title}"
    return f"https://soundcloud.com/search?q={quote(query)}"


def get_youtube_link(track_subtitle, track_title):
    query = f"{track_subtitle} {track_title}"
    search_url = f"https://www.youtube.com/results?search_query={quote(query)}"
    response = requests.get(search_url)
    video_id = None

    # Extracting videoId from YouTube search results page HTML
    start_index = response.text.find('videoId":"') + len('videoId":"')
    end_index = response.text.find('"', start_index)
    if start_index != -1 and end_index != -1:
        video_id = response.text[start_index:end_index]

    if video_id:
        return f"https://www.youtube.com/watch?v={video_id}"
    else:
        return "Nothing found on YouTube"


@bot.message_handler(content_types=['voice'])
def handle_voice_message(message):
    if message.from_user.id == allowed_user_id:
        try:
            file_info = bot.get_file(message.voice.file_id)
            audio_data = bot.download_file(file_info.file_path)

            audio = AudioSegment.from_ogg(BytesIO(audio_data))
            wav_data = audio.export(format="wav").read()

            recognizer = sr.Recognizer()
            with sr.AudioFile(BytesIO(wav_data)) as source:
                audio = recognizer.record(source)

            shazam = Shazam()
            recognize_data = asyncio.run(
                shazam.recognize_song(audio.get_wav_data()))

            if 'track' in recognize_data and recognize_data['track']:
                track_subtitle = recognize_data['track']['subtitle']
                track_title = recognize_data['track']['title']
                response_text = f"Music recognized: {track_subtitle} - {track_title}"

                spotify_link = get_spotify_link(track_subtitle, track_title)
                soundcloud_link = get_soundcloud_link(
                    track_subtitle, track_title)
                youtube_link = get_youtube_link(track_subtitle, track_title)

                bot.send_message(message.chat.id, response_text)
                bot.send_message(
                    message.chat.id, f"Link to search for track on Spotify: {spotify_link}")
                bot.send_message(
                    message.chat.id, f"Link to search for a track on SoundCloud: {soundcloud_link}")
                bot.send_message(
                    message.chat.id, f"Link to search for track on YouTube: {youtube_link}")

            else:
                bot.send_message(
                    message.chat.id, "The music could not be recognized. Check Shazam API data.")
        except Exception as e:
            bot.send_message(message.chat.id, f"An error has occurred: {e}")
    else:
        bot.send_message(
            message.chat.id, "Access denied. You are not authorized to use this bot.")


@bot.message_handler(commands=['start'])
def handle_start(message):
    if message.from_user.id == allowed_user_id:
        bot.send_message(
            message.chat.id, 'Hello! Send a voice message with music and I will recognize the track and find it on Spotify, SoundCloud and YouTube.')
    else:
        bot.send_message(
            message.chat.id, "Access denied. You are not authorized to use this bot.")


@bot.message_handler(content_types=['text'])
def c_text(message):
    if message.from_user.id == allowed_user_id:
        bot.send_message(
            message.chat.id, "Sorry. I can only shazam voice messages. Send me voice message please!")
    else:
        bot.send_message(
            message.chat.id, "Access denied. You are not authorized to use this bot.")


max_attempts = 2
current_attempt = 0

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        current_attempt += 1
        print(f"An error has occurred: {str(e)}")
        if current_attempt >= max_attempts:
            print(
                "The maximum number of attempts has been reached. Stopping the application.")
            break
        else:
            print(
                f"Trying to get the update again. Attempt №{current_attempt}")
            time.sleep(15)  # Пауза перед повторной попыткой
