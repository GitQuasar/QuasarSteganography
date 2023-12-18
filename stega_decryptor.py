# importing module Image from PIL (Python Imaging Library) in order to work with images (to read them, to be exact)
from PIL import Image

# importing module required for doing fun stuff with strings
from textwrap import wrap


# function that generates a special code from user input
def gen(key):
    code = 0
    arr = wrap(key, 2)
    for i in range(4): code += int(arr[i])
    return code

# main function where all fun stuff happens
def imageDecrypt(filepath):
    img = Image.open(filepath)  # create an object of an image
    rgb_img = img.convert('RGB')  # convert it to RGB
    width = img.size[0]  # image width
    height = img.size[1]  # image height

    # first - get a decryption key from a user input
    user_key = str(input("#-> Enter a key: "))
    resulted_key = bin(gen(user_key))[2:].zfill(8)

    # second - get a phraze length from the reserved area of the image
    n = 0
    phraze_length_bin = ""  # binary value with fixed length of 15 on output
    for j in range(0, width):
        remainder = 15 - n
        match remainder:
            case 0:
                break
            case _:
                r = bin(rgb_img.getpixel((j, height - 1))[0])[-1]
                g = bin(rgb_img.getpixel((j, height - 1))[1])[-1]
                b = bin(rgb_img.getpixel((j, height - 1))[2])[-1]

                phraze_length_bin += r + g + b
                n += 3
    phraze_length = int(phraze_length_bin, 2)

    # third - get a binary code of the encrypted phraze from pixel's (r,g,b) values (from the low bits)
    is_done = False
    n = 0
    encrypted_binary_phraze = ""
    for i in range(0, height - 1):
        for j in range(0, width):
            remainder = phraze_length * 5 - n  # make a check that index is not out of range
            match remainder:
                # if the required length has been obtained - exit loops
                case 0:
                    is_done = True
                    break
                # if not - continue reading
                case _:
                    # read the low bits of (r,g,b) binary values of the pixel
                    r = bin(rgb_img.getpixel((j, i))[0])[-1]
                    g = bin(rgb_img.getpixel((j, i))[1])[-1]
                    b = bin(rgb_img.getpixel((j, i))[2])[-1]
                    encrypted_binary_phraze += r + g + b
                    n += 1
        if is_done:
            break

    # fourth - XOR-ing encrypted binary digit-by-digit with the digits of the key
    user_key_index = 0
    encrypted_binary_phraze_length = len(encrypted_binary_phraze)
    binary_phraze = []
    for i in range(0, encrypted_binary_phraze_length):
        if user_key_index >= len(resulted_key):
            user_key_index = 0
        binary_phraze.append(bin(int(encrypted_binary_phraze[i], 2) ^ int(resulted_key[user_key_index], 2))[2:])
        user_key_index += 1

    # fifth - read each 15 digits, convert resulted binary value to UTF-8 code, append the corresponding symbol to the array
    phraze = []
    for i in range(0, len(binary_phraze), 15):
        phraze.append(chr(int(''.join(binary_phraze[i:i+15]), 2)))

    # sixth - # print the message to the console
    print("#OK# The encrypted message is:\n", ''.join(phraze))