from tkinter import *
import io
import base64

icon_data = """
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
i+zmAgIAOw==
"""

def get_photo_image4icon():
    return PhotoImage(data=icon_data)  # PhotoImageオブジェクトの作成

def get_img():
    image_data = base64.b64decode(icon_data)
    return io.BytesIO(image_data)
