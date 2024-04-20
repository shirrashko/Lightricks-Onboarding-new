from functools import partial
import numpy as np
from source.custom_image import CustomImage
from filters import BlurFilter, EdgeDetectionFilter, SharpenFilter
from PIL import ImageEnhance, ImageOps
from source.enums import FilterName, AdjustmentType
from PIL import Image


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
            FilterName.BLUR.value: BlurFilter(),
            FilterName.EDGE_DETECTION.value: EdgeDetectionFilter(),
            FilterName.SHARPEN.value: SharpenFilter(),
        }

    def apply_filter(self, filter_name: str, strength: float) -> None:
        """
        Applies a specified filter to the image.

        Args:
            filter_name (str): The name of the filter to apply.
            strength (float): The strength of the filter to apply.

        Raises:
            ValueError: If the filter name is not supported.
        """
        if filter_name in self.filters:
            filter_instance = self.filters[filter_name]
            for i in range(int(strength)):
                filter_instance.apply(self.custom_image)

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
        adjustment_methods = {
            AdjustmentType.BRIGHTNESS.value: self._adjust_brightness,
            AdjustmentType.CONTRAST.value: self._adjust_contrast,
            AdjustmentType.SATURATION.value: self._adjust_saturation,
        }

        if adjustment in adjustment_methods:
            # Create a partially applied function with the current value
            adjust_func = partial(adjustment_methods[adjustment], value)
            adjust_func()  # Call the partially applied function
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

    def _adjust_brightness(self, brightness_value: float) -> None:
        """
        Adjusts the image brightness by adding a brightness_value to all pixels.

        A positive brightness_value brightens the image, while a negative value darkens it.
        The brightness_value is added to each of the R, G, and B channels of the image.

        Args:
            brightness_value (float): The value to add to each pixel's color value.
                                      Typical range is [-255, 255]. Values outside this range
                                      may lead to clipping where pixel values are pushed to the
                                      minimum or maximum value (0 or 255).
        """
        image_array = np.asarray(self.custom_image.convert_to_rgb().get_image(), dtype=np.float32)

        # Apply brightness adjustment by adding the value
        image_array = np.clip(image_array + brightness_value, 0, 255)

        # Convert back to Image and save to custom_image
        self.custom_image.set_image(Image.fromarray(image_array.astype("uint8")))

    def _adjust_contrast(self, contrast_factor: float) -> None:
        """
        Adjusts the image contrast by blending the original image with an auto-contrasted version of the image.

        Args:
            contrast_factor (float): The factor by which to adjust the contrast. A value of 1.0
                                     means no change, while greater than 1.0 increases contrast and less
                                     than 1.0 but greater than 0 decreases contrast.
        """
        image = self.custom_image.convert_to_rgb().get_image()
        enhanced_image = ImageOps.autocontrast(image, cutoff=0, ignore=None)
        contrast_image = Image.blend(enhanced_image, image, contrast_factor)
        self.custom_image.set_image(contrast_image)

    def _adjust_saturation(self, saturation_factor: float) -> None:
        """
        Adjusts the image saturation.

        Args:
            saturation_factor (float): The factor by which to adjust the saturation. A value of 1.0
                                       means no change, values greater than 1.0 enhance saturation, and
                                       values between 0 and 1.0 reduce saturation.
        """
        image = self.custom_image.convert_to_rgb().get_image()
        converter = ImageEnhance.Color(image)
        saturation_image = converter.enhance(saturation_factor)
        self.custom_image.set_image(saturation_image)
