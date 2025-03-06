from PIL import Image
import numpy as np
import os

def decode_audio_from_image(image_path, output_audio_path):
    # Load the encoded image
    encoded_image = Image.open(image_path)
    image_data = np.array(encoded_image)

    # Flatten the image data
    flat_image = image_data.flatten()

    # Extract the least significant bits of all pixels
    lsb_array = flat_image & 1

    # Extract the first 32 bits for the audio size prefix
    audio_size_bits = lsb_array[:32]
    audio_size = int(''.join(map(str, audio_size_bits)), 2)
    print(f"Decoded audio size (in bytes): {audio_size}")

    # Validate the audio size
    if audio_size <= 0 or audio_size > len(lsb_array[32:]) // 8:
        raise ValueError("Invalid audio size. Decoded data might be corrupted.")

    # Extract the audio data bits
    total_audio_bits = audio_size * 8
    audio_data_bits = lsb_array[32:32 + total_audio_bits]

    # Convert bits to bytes in batches of 8
    audio_bytes = np.packbits(audio_data_bits)

    # Write the decoded audio data to a file
    with open(output_audio_path, "wb") as audio_file:
        audio_file.write(audio_bytes)
    print(f"Audio successfully decoded into {output_audio_path}")
