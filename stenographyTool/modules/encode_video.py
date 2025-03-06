from PIL import Image
import cv2
import numpy as np

def encode_video_into_image(image_path, video_path, output_image_path):
    # Open the image
    img = Image.open(image_path).convert("RGB")
    pixels = np.array(img)

    # Read the video file as binary data
    with open(video_path, "rb") as video_file:
        video_data = video_file.read()

    # Convert the video binary data into a binary string
    binary_data = ''.join(format(byte, '08b') for byte in video_data)
    data_length = len(binary_data)

    # Ensure the image can hold the video data
    max_capacity = pixels.shape[0] * pixels.shape[1] * 3  # Total RGB values
    if data_length + 32 > max_capacity:
        raise ValueError("The image is too small to store the video data.")

    # Prepend the length of the binary data (32 bits)
    length_binary = format(data_length, '032b')
    binary_data = length_binary + binary_data

    # Embed binary data into the image
    index = 0
    for row in range(pixels.shape[0]):
        for col in range(pixels.shape[1]):
            for channel in range(3):  # RGB channels
                if index < len(binary_data):
                    # Replace the least significant bit (LSB) with a bit from the binary data
                    pixel_binary = format(pixels[row, col, channel], '08b')
                    pixels[row, col, channel] = int(pixel_binary[:-1] + binary_data[index], 2)
                    index += 1
                else:
                    break
            if index >= len(binary_data):
                break
        if index >= len(binary_data):
            break

    # Save the modified image
    encoded_image = Image.fromarray(pixels)
    encoded_image.save(output_image_path, "PNG")
    print(f"Video successfully encoded into {output_image_path}")
