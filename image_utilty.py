import os
import base64
import tkinter as tk

from tkinter import filedialog
from typing import Any

from PIL import Image


class ImageHandler:

    @classmethod
    def encode(cls, filename) -> base64:
        with open(filename, "rb") as imageFile:
            encoded_str = base64.b64encode(imageFile.read())
            return encoded_str

    @classmethod
    def decode(cls, encoded_img) -> Any:
        if encoded_img:
            image_64_decode = base64.b64decode(cls.encode(encoded_img))
            # create a writable image and write the decoding result
            with open('Pictures/test_decode.jpeg', 'wb') as image_result:
                image_result.write(image_64_decode)
            return image_result.name
        else:
            return None

    @classmethod
    def open_decoded(cls, img_path) -> None:
        with Image.open(img_path) as my_image:
            my_image.show()

    @classmethod
    def select(cls) -> Any:
        root = tk.Tk()
        root.withdraw()
        filename = filedialog.askopenfilename(initialdir=os.getcwd(
        ), title="Select file", filetypes=(("jpeg images", ".jpeg"), ("all files", "*.*")))
        if not filename:
            print("no such file")
            return None
        else:
            return filename

# if __name__ == '__main__':
#     # ImageHandler().open_decoded(ImageHandler().decode(ImageHandler().select()))
#     object_ob = ImageHandler()
#     img = object_ob.encode("Pictures/test.jpeg")
#     img = object_ob.decode(img)
#     object_ob.open_decoded(img)
