from PIL import Image
import numpy as np
import os

# Function to encode audio into image
def encode_audio_into_image(image_path, audio_path, output_image_path):
    # Load the image
    image = Image.open(image_path).convert("RGB")
    image_data = np.array(image)

    # Read the audio file as binary
    with open(audio_path, "rb") as audio_file:
        audio_data = audio_file.read()

    # Add a size prefix to the audio data
    audio_size = len(audio_data)
    audio_bits = f"{audio_size:032b}" + ''.join(f"{byte:08b}" for byte in audio_data)

    # Check capacity: Maximum number of bits we can embed in the image
    max_bits = image_data.size * 3  # RGB channels can store 3 bits per pixel
    if len(audio_bits) > max_bits:
        raise ValueError("Audio data is too large to encode in this image.")

    # Embed the audio bits in the RGB channels
    flat_image = image_data.reshape(-1, 3)
    for i, bit in enumerate(audio_bits):
        channel = i % 3  # Cycle through R, G, B channels
        pixel_index = i // 3
        flat_image[pixel_index, channel] = (flat_image[pixel_index, channel] & 0xFE) | int(bit)

    # Save the encoded image as a lossless PNG
    encoded_image = flat_image.reshape(image_data.shape)
    encoded_image = Image.fromarray(encoded_image)
    encoded_image.save(output_image_path, format="PNG")
    print(f"Audio successfully encoded into {output_image_path}")
