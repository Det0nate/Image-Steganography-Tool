from PIL import Image
import numpy as np

def decode_video_from_image(image_path, output_video_path):
    # Open the image
    img = Image.open(image_path).convert("RGB")
    pixels = np.array(img)

    binary_data = ''

    # Extract binary data from the image
    for row in range(pixels.shape[0]):
        for col in range(pixels.shape[1]):
            for channel in range(3):  # RGB channels
                binary_data += format(pixels[row, col, channel], '08b')[-1]

    # Extract the length of the data from the first 32 bits
    data_length = int(binary_data[:32], 2)
    video_binary_data = binary_data[32:32 + data_length]

    # Convert the binary data to bytes
    video_bytes = bytearray(int(video_binary_data[i:i + 8], 2) for i in range(0, len(video_binary_data), 8))

    # Save the extracted video data
    with open(output_video_path, "wb") as video_file:
        video_file.write(video_bytes)

    print(f"Video successfully decoded into {output_video_path}")
