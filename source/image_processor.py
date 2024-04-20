from source.custom_image import CustomImage
from filters import BlurFilter, EdgeDetectionFilter, SharpenFilter
from PIL import ImageEnhance


class ImageProcessor:
    """
    Handles applying various filters and adjustments to an image.

    Attributes:
        custom_image (CustomImage): An instance of CustomImage containing the image to process.
        filters (dict): A dictionary mapping filter names to their corresponding filter instances.
    """

    def __init__(self, image_path: str) -> None:
        """
        Initializes the ImageProcessor with an image and sets up available filters.

        Args:
            image_path (str): The path to the image to be processed.
        """
        self.custom_image = CustomImage(image_path)
        self.filters = {
            "blur": BlurFilter(),
            "edge_detection": EdgeDetectionFilter(),
            "sharpen": SharpenFilter()
        }
        self.adjustments = {
            "brightness": ImageEnhance.Brightness,
            "contrast": ImageEnhance.Contrast,
            "saturation": ImageEnhance.Color
        }

    def apply_filter(self, filter_name: str, strength: float) -> None: # todo: add strength parameter logic
        """
        Applies a specified filter to the image.

        Args:
            filter_name (str): The name of the filter to apply.

        Raises:
            ValueError: If the filter name is not supported.
        """
        if filter_name in self.filters:
            filter_instance = self.filters[filter_name]
            self.custom_image.set_image(filter_instance.apply(self.custom_image))
        else:
            raise ValueError(f"Filter '{filter_name}' not supported.")

    def adjust_image(self, adjustment: str, value: float) -> None:
        """
        Adjusts an image property, such as brightness, contrast, or saturation.

        Args:
            adjustment (str): The type of adjustment to apply.
            value (float): The degree to which the adjustment should be applied.

        Raises:
            ValueError: If the adjustment type is not supported.
        """
        if adjustment in self.adjustments:
            enhancer = self.adjustments[adjustment](self.custom_image.get_image())
            self.custom_image.image = enhancer.enhance(value)
        else:
            raise ValueError(f"Adjustment type '{adjustment}' not supported.")

    def save_image(self, path: str) -> None:
        """
        Saves the processed image to the specified path.

        Args:
            path (str): The file path where the image will be saved.
        """
        self.custom_image.save(path)

    def display_image(self) -> None:
        """
        Displays the processed image using the default image viewer.
        """
        self.custom_image.show()
