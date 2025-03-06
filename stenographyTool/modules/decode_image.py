from PIL import Image
from cryptography.fernet import Fernet

def decode_image(image_path, decryption_key=None):
    """
    Decodes the hidden binary message from the image.
    If a decryption key is provided, attempts to decrypt the message.
    """
    # Open the image
    img = Image.open(image_path)
    pixels = img.load()

    binary_message = ''
    img_width, img_height = img.size

    # Traverse through the pixels and extract the LSB from each channel
    for y in range(img_height):
        for x in range(img_width):
            pixel = list(pixels[x, y])

            for i in range(3):  # Loop through RGB channels
                binary_message += str(pixel[i] & 1)

                # Check for the end delimiter
                if binary_message.endswith('1111111111111110'):  # End delimiter
                    # Remove the delimiter
                    binary_message = binary_message[:-16]

                    # Convert binary to text
                    decoded_message = ''.join(
                        chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8)
                    )

                    if decryption_key:
                        # Attempt to decrypt using the provided key
                        try:
                            cipher = Fernet(decryption_key)
                            decrypted_message = cipher.decrypt(decoded_message.encode()).decode()
                            return decrypted_message
                        except Exception as e:
                            raise ValueError("Decryption failed. Check the encryption key.") from e
                    else:
                        # Return the plain decoded message if no key is provided
                        return decoded_message

    # If no delimiter is found
    raise ValueError("End delimiter not found. Decoding failed.")
