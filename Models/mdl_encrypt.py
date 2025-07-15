import datetime
from pathlib import Path
from textwrap import wrap
from PIL import Image, ImageDraw, ImageFile


class ImageEncryptor:  # pylint: disable=R0902
    """
    ImageEncryptor model.

    A class for encrypting text messages into images using steganography.
    Encrypts text by embedding binary data into the least significant bits of RGB pixel values.
    Uses current date to generate encryption key and stores message length in the last row of pixels.
    """

    def __init__(self):
        self._path_in: Path
        self._image: ImageFile.ImageFile
        self._image_width: int = 0
        self._image_height: int = 0
        self._text: str = ""
        self._text_length: int = 0
        self._text_bin: str = ""

    def _gen_key_from_date(self):
        date = str(datetime.date.today()).replace("-", "")
        key = 0
        arr = wrap(date, 2)
        for i in range(0, 5):
            arr.insert(0, arr.pop())
        for i in range(4):
            key += int(arr[i])

        return key

    def _encrypt_text(self, key: str) -> list:
        index = 0
        array_bin = []
        for i, value in enumerate(self._text_bin):  # pylint: disable=W0612
            if index >= len(key):
                index = 0
            array_bin.append(bin(int(value, 2) ^ int(key[index], 2))[2:])
            index += 1

        return array_bin

    def _draw_text_to_image(
        self,
        char_array: list,
        img_rgb_in: ImageFile.ImageFile,
        draw_obj_out: ImageDraw.ImageDraw,
    ) -> ImageDraw.ImageDraw:
        n = 0
        is_done = False
        for i in range(0, self._image_height - 1):
            for j in range(0, self._image_width):
                remainder = len(char_array) - n
                match remainder:
                    case 0:
                        is_done = True
                        break
                    case _:
                        r: str = bin(img_rgb_in.getpixel((j, i))[0])[2:]
                        g: str = bin(img_rgb_in.getpixel((j, i))[1])[2:]
                        b: str = bin(img_rgb_in.getpixel((j, i))[2])[2:]
                        # replace low bits of the binary values
                        r = int(r[0:-1] + char_array[n], 2)
                        g = int(g[0:-1] + char_array[n + 1], 2)
                        b = int(b[0:-1] + char_array[n + 2], 2)

                        draw_obj_out.point((j, i), (r, g, b))
                        n += 3
            if is_done:
                break

        return draw_obj_out

    def _draw_key_to_image(
        self, img_rgb_in: ImageFile.ImageFile, draw_obj_out: ImageDraw.ImageDraw
    ) -> ImageDraw.ImageDraw:
        text_length_bin = bin(self._text_length)[2:].zfill(15)
        n = 0
        for j in range(0, self._image_width):
            remainder = len(text_length_bin) - n
            match remainder:
                case 0:
                    break
                case _:
                    r = bin(img_rgb_in.getpixel((j, self._image_height - 1))[0])[2:]
                    g = bin(img_rgb_in.getpixel((j, self._image_height - 1))[1])[2:]
                    b = bin(img_rgb_in.getpixel((j, self._image_height - 1))[2])[2:]

                    r = int(r[0:-1] + text_length_bin[n], 2)
                    g = int(g[0:-1] + text_length_bin[n + 1], 2)
                    b = int(b[0:-1] + text_length_bin[n + 2], 2)

                    draw_obj_out.point((j, self._image_height - 1), (r, g, b))
                    n += 3

        return draw_obj_out

    def encrypt(self, text: str, path_in: Path):
        # self._test_path: Path = Path(__file__).resolve().name
        self._text = text
        self._text_length = len(text)
        if self._text_length == 0:
            print("No message provided.")
            return
        if "\\" in self._text:
            print("Backslash isn't allowed.")
            return

        self._path_in = path_in.resolve()
        self._image = Image.open(str(self._path_in))
        self._image_width = self._image.width
        self._image_height = self._image.height

        for i in range(0, self._text_length):
            self._text_bin += bin(ord(self._text[i]))[2:].zfill(15)

        image_rgb: Image.Image = self._image.convert("RGB")
        draw_object: ImageDraw.ImageDraw = ImageDraw.Draw(self._image)
        key = bin(self._gen_key_from_date())[2:].zfill(8)
        array_bin_encrypted: list = self._encrypt_text(key)
        draw_object = self._draw_text_to_image(
            array_bin_encrypted, image_rgb, draw_object
        )
        draw_object = self._draw_key_to_image(image_rgb, draw_object)

        path_out = self._path_in.with_name(f"out_{self._path_in.name}")
        self._image.save(path_out, "PNG")
        # print("Image has been processed and stored in: ", path_out)

        return path_out
