from PIL import Image

def encode_image(image_path, message, output_image_path):
    # Open the image
    img = Image.open(image_path)
    pixels = img.load()

    # Convert the message into binary format
    binary_message = ''.join(format(ord(i), '08b') for i in message) + '1111111111111110'  # End delimiter
    message_length = len(binary_message)
    img_width, img_height = img.size

    # Ensure the image has enough pixels to store the message
    if message_length > img_width * img_height * 3:
        raise ValueError("Image is too small to hold the message.")

    # Traverse through the pixels and embed the message
    binary_index = 0
    for y in range(img_height):
        for x in range(img_width):
            pixel = list(pixels[x, y])

            for i in range(3):  # Loop through RGB channels
                if binary_index < message_length:
                    pixel[i] = (pixel[i] & ~1) | int(binary_message[binary_index])
                    binary_index += 1

            pixels[x, y] = tuple(pixel)
            if binary_index >= message_length:
                break
        if binary_index >= message_length:
            break

    # Save the new image with the hidden message
    img.save(output_image_path)
    print(f"Message successfully hidden in {output_image_path}")
