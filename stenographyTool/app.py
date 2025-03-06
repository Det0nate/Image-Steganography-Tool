import os
from pydub import AudioSegment 
from flask import Flask, render_template, request, redirect, url_for, flash
from modules.encode_image import encode_image
from modules.decode_image import decode_image
from modules.encrypt_decrypt_message import generate_key, encrypt_message, decrypt_message
from modules.encode_video import encode_video_into_image
from modules.decode_video import decode_video_from_image
from modules.encode_audio import encode_audio_into_image
from modules.decode_audio import decode_audio_from_image

app = Flask(__name__)
app.secret_key = "your_secret_key"  # For flash messages

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/text_in_image")
def text_in_image():
    return render_template("text_in_image.html")

@app.route("/video_in_image")
def video_in_image():
    return render_template("video_in_image.html")

@app.route("/audio_in_image")
def audio_in_image():
    return render_template("audio_in_image.html")


@app.route("/encode", methods=["POST"])
def encode():
    if "image" not in request.files or not request.form.get("message"):
        flash("Please provide an image and a message.")
        return redirect(url_for("error"))

    image = request.files["image"]
    message = request.form["message"]
    encryption = request.form.get("encryption") == "on"

    # Save uploaded image temporarily
    input_image_path = f"static/encoded_images/{image.filename}"
    image.save(input_image_path)

    output_image_path = f"static/encoded_images/encoded_{image.filename}"
    if encryption:
        key = generate_key()
        encrypted_message = encrypt_message(message, key)
        encode_image(input_image_path, encrypted_message.decode(), output_image_path)
        return render_template("result.html", output_image=output_image_path, key=key.decode())
    else:
        encode_image(input_image_path, message, output_image_path)
        return render_template("error.html", output_image=output_image_path)

@app.route("/decode", methods=["POST"])
def decode():
    if "image" not in request.files:
        flash("Please provide an image to decode.")
        return redirect(url_for("error"))

    image = request.files["image"]
    decryption_key = request.form.get("key")

    # Save uploaded image temporarily
    image_path = f"static/encoded_images/{image.filename}"
    image.save(image_path)

    try:
        decoded_message = decode_image(image_path, decryption_key)
        return render_template("result.html", decoded_message=decoded_message)
    except ValueError as e:
        flash(str(e))
        return redirect(url_for("error"))
    
@app.route("/encode_video", methods=["POST"])
def encode_video():
    if "image" not in request.files or "video" not in request.files:
        flash("Please provide both an image and a video file.")
        return redirect(url_for("error"))

    image = request.files["image"]
    video = request.files["video"]

    input_image_path = f"static/{image.filename}"
    video_path = f"static/encoded_videos/{video.filename}"
    output_image_path = f"static/encoded_videos/encoded_{image.filename}"

    image.save(input_image_path)
    video.save(video_path)

    try:
        encode_video_into_image(input_image_path, video_path, output_image_path)
        return render_template("result.html", output_image=output_image_path)
    except ValueError as e:
        flash(str(e))
        return redirect(url_for("error"))

@app.route("/decode_video", methods=["POST"])
def decode_video():
    if "image" not in request.files:
        flash("Please provide an image to decode.")
        return redirect(url_for("error"))

    image = request.files["image"]
    output_video_path = "static/decoded_video.mp4"

    image_path = f"static/{image.filename}"
    image.save(image_path)

    try:
        decode_video_from_image(image_path, output_video_path)
        return render_template("result.html", decoded_video=output_video_path)
    except ValueError as e:
        flash(str(e))
        return redirect(url_for("error"))


@app.route("/encode_audio", methods=["POST"])
def encode_audio():
    if "image" not in request.files or "audio" not in request.files:
        return render_template("error.html", message="Please provide both an image and an audio file.")

    image = request.files["image"]
    audio = request.files["audio"]

    # Check if the uploaded audio file is an MP3
    if not audio.filename.lower().endswith(".mp3"):
        return render_template("error.html", message="Only MP3 files are supported.")

    input_image_path = f"static/{image.filename}"
    audio_path = f"static/encoded_audio/{audio.filename}"
    output_image_path = f"static/encoded_audio/encoded_{image.filename}"

    os.makedirs("static/encoded_audio", exist_ok=True)
    image.save(input_image_path)
    audio.save(audio_path)

    try:
        encode_audio_into_image(input_image_path, audio_path, output_image_path)
        return render_template("result.html", output_image=output_image_path)
    except ValueError as e:
        return render_template("error.html", message=f"Error encoding audio: {str(e)}")


@app.route("/decode_audio", methods=["POST"])
def decode_audio():
    image = request.files.get("encoded_image")  # Match the form input name
    if not image:
        print("No image file found in the request!")  # Debugging log
        return render_template("error.html", message="Please provide an image to decode.")

    output_audio_path = "static/decoded_audio/decoded_audio.mp3"
    os.makedirs("static/decoded_audio", exist_ok=True)

    image_path = f"static/{image.filename}"
    image.save(image_path)

    try:
        decode_audio_from_image(image_path, output_audio_path)
        return render_template("result.html", decoded_audio=output_audio_path)
    except ValueError as e:
        return render_template("error.html", message=f"Error decoding audio: {str(e)}")



if __name__ == "__main__":
    app.run(debug=True)
