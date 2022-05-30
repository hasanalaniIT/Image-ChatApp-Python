import os
import base64
import tkinter as tk

from tkinter import filedialog
from PIL import Image


class ImageHandler:

    @classmethod
    def encode(cls, filename) -> base64:
        with open(filename, "rb") as imageFile:
            encoded_str = base64.b64encode(imageFile.read())
            return encoded_str

    @classmethod
    def decode(cls, encoded_img):
        image_64_decode = base64.b64decode(cls.encode(encoded_img))
        # create a writable image and write the decoding result
        with open('Pictures/test_decode.jpeg', 'wb') as image_result:
            image_result.write(image_64_decode)
        return "test_decode.jpeg"

    @classmethod
    def open_decoded(cls, img_path) -> None:
        with Image.open("Pictures/" + img_path) as my_image:
            my_image.show()

    @classmethod
    def select(cls) -> str:
        root = tk.Tk()
        root.withdraw()
        filename = filedialog.askopenfilename(initialdir=os.getcwd(
        ), title="Select file", filetypes=(("jpeg images", ".jpeg"), ("all files", "*.*")))
        if not filename:
            return "no such file"
        else:
            return filename


# ImageHandler().open_decoded(ImageHandler().decode(ImageHandler().select()))
