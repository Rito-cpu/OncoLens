from .app_config import *


class Functions:
    # SET SVG ICON
    def set_svg_icon(icon_name):
        svg_icon_folder = IMG_RSC_PATH / "svg_icons"
        icon = svg_icon_folder / icon_name
        return str(icon)

    # SET SVG IMAGE
    def set_svg_image(image_name):
        svg_image_folder = IMG_RSC_PATH / "svg_images"
        icon = svg_image_folder / image_name
        return str(icon)

    # SET IMAGE
    def set_image(image_name):
        image_folder = IMG_RSC_PATH / "downloads"
        image = image_folder / image_name
        return str(image)