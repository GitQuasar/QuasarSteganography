from textwrap import wrap
from pathlib import Path

from PIL import Image, ImageFile


class ImageDecryptor:
    """
    ImageDecryptor model.

    A class for decrypting text messages hidden in images using steganography.
    Extracts encrypted text from RGB pixel values and decrypts it using a user-provided key.
    """

    def __init__(self):
        self._path_in: Path
        self._image: ImageFile.ImageFile
        self._image_width: int = 0
        self._image_height: int = 0

    def _gen_code_from_key(self, key: str):
        code = 0
        arr = wrap(key, 2)
        try:
            for i in range(4):
                code += int(arr[i])
        except ValueError:
            code = 0
        return code

    def _get_text_length_from_image(self, img_rgb_in: ImageFile.ImageFile):
        n = 0
        text_length_bin = ""  # binary value with fixed length of 15 on output
        for j in range(0, self._image_width):
            remainder = 15 - n
            match remainder:
                case 0:
                    break
                case _:
                    r = bin(img_rgb_in.getpixel((j, self._image_height - 1))[0])[-1]
                    g = bin(img_rgb_in.getpixel((j, self._image_height - 1))[1])[-1]
                    b = bin(img_rgb_in.getpixel((j, self._image_height - 1))[2])[-1]
                    text_length_bin += r + g + b
                    n += 3

        return int(text_length_bin, 2)

    def _get_encrypted_text_from_image(
        self, img_rgb_in: ImageFile.ImageFile, text_length: int
    ):
        n = 0
        is_done = False
        text_bin_encrypted = ""
        for i in range(0, self._image_height - 1):
            for j in range(0, self._image_width):
                remainder = text_length * 5 - n
                match remainder:
                    case 0:
                        is_done = True
                        break
                    case _:
                        r = bin(img_rgb_in.getpixel((j, i))[0])[-1]
                        g = bin(img_rgb_in.getpixel((j, i))[1])[-1]
                        b = bin(img_rgb_in.getpixel((j, i))[2])[-1]
                        text_bin_encrypted += r + g + b
                        n += 1
            if is_done:
                break

        return text_bin_encrypted

    def _decrypt_text_bin(self, char_array: list, text_bin_encrypted: str, code: str):
        text = []
        index = 0
        for i, value in enumerate(text_bin_encrypted):  # pylint: disable=W0612
            if index >= len(code):
                index = 0
            char_array.append(bin(int(value, 2) ^ int(code[index], 2))[2:])
            index += 1
        for i in range(0, len(char_array), 15):
            text.append(chr(int("".join(char_array[i : i + 15]), 2)))

        return str("".join(text))

    def decrypt(self, path_in: Path, user_key: str):
        self._path_in = path_in.resolve()
        self._image = Image.open(str(self._path_in))
        self._image_width = self._image.width
        self._image_height = self._image.height

        image_rgb = self._image.convert("RGB")
        if len(user_key) != 8:
            return ""
        code = bin(self._gen_code_from_key(user_key))[2:].zfill(8)
        text_length = self._get_text_length_from_image(image_rgb)
        text_bin_encrypted = self._get_encrypted_text_from_image(image_rgb, text_length)
        text: str = self._decrypt_text_bin([], text_bin_encrypted, code)

        return str(text)
