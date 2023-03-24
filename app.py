from flask import Flask, render_template, request, redirect, url_for
import openai
import requests
import base64
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# Set up OpenAI API credentials
openai.api_key = "YOUR API"

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def generate_postcard():
    # Get the postcard message from the form
    postcard_message = request.form["postcard_message"]

    # Set up the OpenAI DALL-E model parameters
    model_engine = "image-alpha-001"
    num_images = 1
    size = "1024x1024"
    response_format = "url"

    # Generate the image
    response = openai.Image.create(
        model=model_engine,
        prompt=postcard_message,
        n=num_images,
        size=size,
        response_format=response_format,
    )

    # Get the image URL from the response
    image_url = response.data[0]["url"]

    # Load the image from the URL
    image = Image.open(requests.get(image_url, stream=True).raw)

    # Add the postcard message to the image
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", 24)
    text_width, text_height = draw.textsize(postcard_message, font)
    text_position = ((image.width - text_width) / 2, (image.height - text_height) / 2)
    draw.text(text_position, postcard_message, fill=(0, 0, 0), font=font)

    # Save the postcard image to a byte stream
    byte_stream = BytesIO()
    image.save(byte_stream, format="JPEG")
    byte_stream.seek(0)

    # Convert the byte stream to base64 for displaying in the HTML
    base64_image = base64.b64encode(byte_stream.getvalue()).decode()

    return render_template("postcard.html", base64_image=base64_image)

if __name__ == "__main__":
    app.run(debug=True)
