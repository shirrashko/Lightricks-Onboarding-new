from source.custom_image import CustomImage
from filters import BlurFilter, EdgeDetectionFilter, SharpenFilter
from PIL import ImageEnhance


class ImageProcessor:
    def __init__(self, image_path):
        self.custom_image = CustomImage(image_path)
        self.processed_image = CustomImage(image_path)

    def apply_filter(self, filter_name):
        filters = {
            "blur": BlurFilter(),
            "edge_detection": EdgeDetectionFilter(),
            "sharpen": SharpenFilter()
        }
        if filter_name in filters:
            filter_instance = filters[filter_name]
            self.processed_image = filter_instance.apply(self.custom_image)
        else:
            raise ValueError(f"Filter '{filter_name}' not supported.")

    def adjust_image(self, adjustment, value):
        if adjustment == "brightness":
            enhancer = ImageEnhance.Brightness(self.custom_image.image)
        elif adjustment == "contrast":
            enhancer = ImageEnhance.Contrast(self.custom_image.image)
        elif adjustment == "saturation":
            enhancer = ImageEnhance.Color(self.custom_image.image)
        else:
            return  # If adjustment type is unknown, do nothing

        self.processed_image = enhancer.enhance(value)

    def save_image(self, path):
        self.processed_image.save(path)

    def display_image(self):
        self.processed_image.show()
