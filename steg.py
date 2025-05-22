from PIL import Image
import sys

exit_keywords = ['exit', 'quit', 'no', 'q', 'e', 'n', 'abort']

plaintext = input("Enter text string to be embedded into image or 'file' to import text from a file: ")
if plaintext.lower() == 'file':
    plaintext_file = input("Enter text file to be embedded into image: ")
    plaintext = open(plaintext_file).read()
    type(plaintext)

def text_to_bin (plaintext) :
    """
    Convert text string to binary value
    """

    return ''.join(format(ord(char), '08b') for char in plaintext)

ciphertext = text_to_bin(plaintext)
print(ciphertext)

# Open image file and read binary for pixels
print("Note: PNG files recommended, JPEG not recommended (due to lossiness.)")
filename = input("Enter filename for image to be used: ")
if filename in exit_keywords:
    print("Bye bye!")
    sys.exit()
else:
    with Image.open(filename) as input_image:
        # List of all pixel values
        bin_image = list(input_image.getdata())


def encode_image (ciphertext, bin_image):

    """
        Encode ciphertext into LSB of each pixel channel
    """

    mod_pix = []
    cipher_index = 0
    for pixel in bin_image:
        new_pixel = list(pixel)
        for i in range(len(new_pixel)):
            if cipher_index < len(ciphertext):
                if ciphertext[cipher_index] == '1':
                    new_pixel[i] = (new_pixel[i] & ~1) | 1
                elif ciphertext[cipher_index] == '0':
                    new_pixel[i] = new_pixel[i] & ~1
                cipher_index += 1
            else:
                break
        mod_pix.append(tuple(new_pixel))

    return mod_pix

# Encode image with steg_data
steg_image_data = encode_image(ciphertext, bin_image)
print(steg_image_data)

# Write new image file with adjusted pixels and save file
steg_image = Image.new(input_image.mode, input_image.size)
steg_image.putdata(steg_image_data)

new_filename = input("What would you like to save your new image as? ")
try:
    steg_image.save(new_filename, 'PNG')
    print(f"Image saved successfully as {new_filename}")
except Exception as e:
    print(f"Error occurred while saving the image: {e}")

stegfilename = input("Enter a file to decode or exit: ")
if stegfilename.lower() in exit_keywords:
    print("Exiting the program, adios!")
    sys.exit()

def decode_image (stegfilename):

    """
        Extract ciphertext from LSB of each pixel channel
        Decode ciphertext using
    """

    with Image.open(stegfilename) as encoded_image:
        steg_data = list(encoded_image.getdata())
        binary_data = ''
        total_pixels = len(steg_data)
        channels = len(steg_data[0])

        # Access LSB of each pixel and extract ciphertext
        print(f"Decoding {total_pixels} pixels...")
        for pixel_index, pixel in enumerate(steg_data):
            for channel in pixel:
                binary_data += str(channel & 1)
            if pixel_index % (total_pixels // 20) == 0:
                print(f"Progress: {100 * pixel_index // total_pixels}% decoded...")


        print("Decoding complete")
        print("Here's your secret message you so desperately wanted: ")

        byte_data = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]

        decoded_text = ''.join(chr(int(byte, 2)) for byte in byte_data)

        return decoded_text

decoded_text_file = input("Enter filename to save decoded text: ")
# Output decoded data to a text file for searching
with open(decoded_text_file, 'w', encoding = 'utf-8') as output_file:
    decoded_data = decode_image(stegfilename)
    print(decoded_data)
    output_file.write(decoded_data)
    print(f"File saved as {decoded_text_file}.")

