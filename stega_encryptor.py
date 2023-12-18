# importing module Image from PIL (Python Imaging Library) in order to work with images (to read them, to be exact)
# importing module ImageDraw in order to be able to draw pixels on the image
from PIL import Image, ImageDraw

# importing module datetime in order to be able to get an actual date
import datetime

# importing module required for doing fun stuff with strings
from textwrap import wrap

# function that generates a special code from current date
def gen():
    code = 0
    date = str(datetime.date.today()).replace("-", "")
    arr = wrap(date, 2)  # create an array of 2-symbol strings
    for i in range(0, 5):
        arr.insert(0, arr.pop())  # right cycle shift by two digits
    for i in range(4): code += int(arr[i])
    return code

def imageEncrypt(filepath):
    img = Image.open(filepath)  # create an object of an image
    rgb_img = img.convert('RGB')  # convert it to RGB
    width = img.size[0]  # image width
    height = img.size[1]  # image height
    draw = ImageDraw.Draw(img)  # drawing object

    # first - prompt a user to enter his message
    phraze = str(input("#-> Message to encrypt (backslash is not allowed):\n"))

    # second - do some fun checks in order for the program to not drop dead
    phraze_length = len(phraze)
    if phraze_length == 0:
        print("#!# No message to encrypt.")
        return
    if "\\" in phraze:
        print("#!# No backslash is allowed. Sorry.")
        return

    # third - generate an encryption key from current date
    key = bin(gen())[2:].zfill(8)  # date-based key

    # fourth - get a binary code of the entire phraze using UTF-values of the symbols
    phraze_bin = ""
    for character_index in range(0, phraze_length):
        # use length of 15 for convenience
        phraze_bin += bin(ord(phraze[character_index]))[2:].zfill(15)


    # fifth - encrypting phraze's binary contents by XOR-ing every single digit
    # with a digit of previously generated key
    key_index = 0
    len_phraze_bin = len(phraze_bin)
    encrypted_binary_array = []
    for i in range(0, len_phraze_bin):
        # check for range overflow
        if key_index >= len(key):
            key_index = 0
        # appending result of each step to an array
        encrypted_binary_array.append(bin(int(phraze_bin[i], 2) ^ int(key[key_index], 2))[2:])
        key_index += 1

    # sixth - encrypt phraze into the image by writing every third binary digit
    # to the low bits of pixel's (r,g,b) values
    is_done = False
    n = 0
    for i in range(0, height - 1):  # encrypting message
        for j in range(0, width):
            remainder = len(encrypted_binary_array) - n
            match remainder:
                # if the required length has been obtained - exit loops
                case 0:
                    is_done = True
                    break
                # if not - continue reading
                case _:
                    # read (r,g,b) binary values of the pixel
                    r = bin(rgb_img.getpixel((j, i))[0])[2:]
                    g = bin(rgb_img.getpixel((j, i))[1])[2:]
                    b = bin(rgb_img.getpixel((j, i))[2])[2:]

                    # replace low bits of the binary values
                    r = int(r[0:-1] + encrypted_binary_array[n], 2)
                    g = int(g[0:-1] + encrypted_binary_array[n+1], 2)
                    b = int(b[0:-1] + encrypted_binary_array[n+2], 2)

                    # draw edited pixel to the same coordinates
                    draw.point((j, i), (r, g, b))
                    n += 3
        if is_done:
            break

    # seventh - hide the phraze length in the reserved area of the image by the same algorythm
    phraze_length_bin = bin(phraze_length)[2:].zfill(15)  # binary code of the phraze length
    n = 0
    for j in range(0, width):
        remainder = len(phraze_length_bin) - n
        match remainder:
            case 0:
                break
            case _:
                # read (r,g,b) binary values of the pixel
                r = bin(rgb_img.getpixel((j, height - 1))[0])[2:]
                g = bin(rgb_img.getpixel((j, height - 1))[1])[2:]
                b = bin(rgb_img.getpixel((j, height - 1))[2])[2:]

                # replace low bits of the binary values
                r = int(r[0:-1] + phraze_length_bin[n], 2)
                g = int(g[0:-1] + phraze_length_bin[n + 1], 2)
                b = int(b[0:-1] + phraze_length_bin[n + 2], 2)

                # draw edited pixel to the same coordinates
                draw.point((j, height - 1), (r, g, b))
                n += 3

    # eigth - save the result as a new image
    filename = "output.png"
    img.save(filename, "PNG")
    print("#OK# Image has been processed, new image: ", filename)