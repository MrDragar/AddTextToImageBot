import logging

import cloudinary
from cloudinary import uploader


def init_cloudinary(cloud_name: str, api_key: str, api_secret: str):
    cloudinary.config(
        cloud_name=cloud_name, api_key=api_key, api_secret=api_secret
    )


def add_text_to_image(
        image_path: str, text: str, font_size: int = 50,
        gravity: str = "center", font_family: str = "Arial"
) -> str:
    logging.debug(f"{image_path}, {text}")
    response = cloudinary.uploader.upload(
        image_path,
        transformation=[
            {"overlay": {"font_family": "Arial", "font_size": 50,
                         "text": text}},
            {"flags": "layer_apply", "gravity": "center", "y": 0}
        ]
    )
    logging.debug(response)
    return response["secure_url"]
