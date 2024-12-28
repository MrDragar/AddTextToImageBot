import cloudinary


def init_cloudinary(cloud_name: str, api_key: str, api_secret: str):
    cloudinary.config(
        cloud_name=cloud_name, api_key=api_key, api_secret=api_secret
    )

