import os
import subprocess
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters

TOKEN = "8527038108:AAFil2UBQEcD6OoywsCp5vxJFs5LuagaNJ0"
bot = Bot(token=TOKEN)

app = Flask(__name__)

dispatcher = Dispatcher(bot, None, workers=0, use_context=True)

def start(update, context):
    update.message.reply_text(
        "Send video 📹\nI will compress to HEVC (H.265) without quality loss."
    )

def compress(update, context):
    video = update.message.video
    file = bot.get_file(video.file_id)

    input_file = "input.mp4"
    output_file = "output_hevc.mp4"

    file.download(input_file)
    update.message.reply_text("⏳ Compressing, wait...")

    command = [
        "ffmpeg", "-i", input_file,
        "-c:v", "libx265",
        "-preset", "fast",
        "-crf", "18",
        "-c:a", "copy",
        output_file
    ]

    subprocess.run(command)

    update.message.reply_video(video=open(output_file, "rb"))

    os.remove(input_file)
    os.remove(output_file)

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.video, compress))

@app.route("/", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK"

@app.route("/", methods=["GET"])
def home():
    return "HEVC Bot Running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
