from source.custom_image import CustomImage
from filters import BlurFilter, EdgeDetectionFilter, SharpenFilter


class ImageProcessor:
    def __init__(self, image_path):
        self.custom_image = CustomImage(image_path)

    def apply_filter(self, filter_name):
        filters = {
            "blur": BlurFilter(),
            "edge_detection": EdgeDetectionFilter(),
            "sharpen": SharpenFilter()
        }
        if filter_name in filters:
            filter_instance = filters[filter_name]
            filter_instance.apply(self.custom_image)
        else:
            raise ValueError(f"Filter '{filter_name}' not supported.")

    def save_image(self, path):
        self.custom_image.save(path)

    def display_image(self):
        self.custom_image.show()
