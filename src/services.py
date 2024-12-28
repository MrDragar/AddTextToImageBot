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


def init_cloudinary(cloud_name: str, api_key: str, api_secret: str):
    cloudinary.config(
        cloud_name=cloud_name, api_key=api_key, api_secret=api_secret
    )


def add_text_to_image(
        image_path: str, text: str, font_size: int = 50,
        gravity: str = "center", font_family: str = "Arial",
        **extra
) -> str:
    logging.debug(f"{image_path}, {text}")
    response = cloudinary.uploader.upload(
        image_path,
        transformation=[
            {"overlay": {"font_family": font_family, "font_size": font_size,
                         "text": text}},
            {"flags": "layer_apply", "gravity": gravity, "y": 0}
        ]
    )
    logging.debug(response)
    return response["secure_url"]
