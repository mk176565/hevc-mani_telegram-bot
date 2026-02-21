from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import subprocess
import os

TOKEN = "8527038108:AAFil2UBQEcD6OoywsCp5vxJFs5LuagaNJ0"

def start(update, context):
    update.message.reply_text(
        "Send a video 📹\nI will compress it to HEVC (H.265) without quality loss."
    )

def compress_video(update, context):
    video = update.message.video
    file = context.bot.get_file(video.file_id)

    input_file = "input.mp4"
    output_file = "output_hevc.mp4"

    file.download(input_file)
    update.message.reply_text("⏳ Compressing... Please wait")

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

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.video, compress_video))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
