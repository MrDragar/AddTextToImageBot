import logging

import cloudinary
from cloudinary import uploader


GRAVITY_TRANSLATIONS = {
    "Север": "north",
    "Юг": "south",
    "Центр": "center",
    "Восток": "east",
    "Запад": "west",
}


COLOR_TRANSLATIONS = {
    "Красный": "red",
    "Зеленый": "green",
    "Синий": "blue",
    "Желтый": "yellow",
    "Черный": "black",
    "Белый": "white",
}


def init_cloudinary(cloud_name: str, api_key: str, api_secret: str):
    cloudinary.config(
        cloud_name=cloud_name, api_key=api_key, api_secret=api_secret
    )


def add_text_to_image(
        image_path: str, text: str, font_size: int = 90,
        gravity: str = "center", font_family: str = "Arial",
        text_color: str = "black", **extra
) -> str:
    logging.debug(f"{image_path}, {text}, {font_size}, {gravity}, {font_family}, {text_color}")
    response = cloudinary.uploader.upload(
        image_path,
        transformation=[
            {"overlay": {"font_family": font_family, "font_size": font_size,
                         "text": text}, "color": text_color},
            {"flags": "layer_apply", "gravity": gravity, "y": 0}
        ]
    )
    logging.debug(response)
    return response["secure_url"]
