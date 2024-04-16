from source.custom_image import CustomImage
from filters import BlurFilter, EdgeDetectionFilter, SharpenFilter
from PIL import ImageEnhance


class ImageProcessor:
    def __init__(self, image_path):
        # Initialize with a single CustomImage instance that will be modified directly
        self.custom_image = CustomImage(image_path)

    def apply_filter(self, filter_name):
        filters = {
            "blur": BlurFilter(),
            "edge_detection": EdgeDetectionFilter(),
            "sharpen": SharpenFilter()
        }
        if filter_name in filters:
            filter_instance = filters[filter_name]
            # Apply the filter directly to the CustomImage instance
            self.custom_image.image = filter_instance.apply(self.custom_image)
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
            raise ValueError(f"Adjustment type '{adjustment}' not supported.")

        # Update the image directly in the CustomImage instance
        self.custom_image.image = enhancer.enhance(float(value))

    def save_image(self, path):
        self.custom_image.image.save(path)

    def display_image(self):
        self.custom_image.image.show()
