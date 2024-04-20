import os
import unittest
from source.image_processor import ImageProcessor
import source.enums as enums


class TestImageProcessor(unittest.TestCase):
    def setUp(self):
        """Set up for the test using the content root."""
        # Get the directory of this file/script.
        base_dir = os.path.dirname(__file__)
        # Construct the image path relative to the script location.
        self.image_path = os.path.join(base_dir, "../input/image_to_filter.jpg")
        self.image_path = os.path.normpath(self.image_path)
        # Ensure the output directory path is constructed similarly.
        self.output_path = os.path.normpath(os.path.join(base_dir, "output"))
        self.processor = ImageProcessor(self.image_path)

    def test_initialization_on_success(self):
        """Test that initialization with a valid path does not raise an exception"""
        try:
            ImageProcessor(self.image_path)
        except IOError as e:
            self.fail(f"Initialization with a valid image path raised an IOError: {e}")

    def test_load_image_on_failure(self):
        """Test that initializing with a non-existent image path raises an IOError"""
        with self.assertRaises(IOError) as context:
            ImageProcessor("path/to/nonexistent/image.jpg")
        self.assertIn("unable to open image: ", str(context.exception).lower())

    def test_apply_filter_on_success(self):
        """Test that applying a filter does not raise an exception"""
        try:
            self.processor.apply_filter(enums.FilterName.BLUR.value, 1)
            self.processor.apply_filter(enums.FilterName.SHARPEN.value, 1)
            self.processor.apply_filter(enums.FilterName.EDGE_DETECTION.value, 1)
        except Exception as e:
            self.fail(f"Applying filter raised an exception {e}")

    def test_apply_filter_on_failure(self):
        """Test that applying an invalid filter raises a ValueError"""
        with self.assertRaises(ValueError) as context:
            self.processor.apply_filter("invalid_filter", 1)
        self.assertIn("not supported", str(context.exception).lower())
        self.assertIn("filter", str(context.exception).lower())

    def test_apply_blur_filter(self):
        """Test the blur filter"""
        try:
            self.processor.apply_filter(enums.FilterName.BLUR.value, 1)
            self.processor.save_image(self.output_path + "/blurred_image_result.jpg")
        except Exception as e:
            self.fail(f"Applying blur filter raised an exception {e}")

    def test_apply_edge_detection_filter(self):
        """Test the edge detection filter"""
        try:
            self.processor.apply_filter(enums.FilterName.EDGE_DETECTION.value, 1)
            self.processor.save_image(self.output_path + "/edge_detected_image_result.jpg")
        except Exception as e:
            self.fail(f"Applying edge detection filter raised an exception {e}")

    def test_apply_sharpen_filter(self):
        """Test the sharpen filter"""
        try:
            self.processor.apply_filter(enums.FilterName.SHARPEN.value, 1)
            self.processor.save_image(self.output_path + "/sharpened_image_result.jpg")
        except Exception as e:
            self.fail(f"Applying sharpen filter raised an exception {e}")

    def test_adjust_image_on_success(self):
        """Test image adjustments do not raise exceptions"""
        try:
            self.processor.adjust_image(enums.AdjustmentType.BRIGHTNESS.value, 1.5)
            self.processor.adjust_image(enums.AdjustmentType.CONTRAST.value, 1.5)
            self.processor.adjust_image(enums.AdjustmentType.SATURATION.value, 1.5)
        except Exception as e:
            self.fail(f"Adjusting image raised an exception {e}")

    def test_adjust_image_on_value_error(self):
        """Test that adjusting an image with an invalid adjustment type raises a ValueError"""
        with self.assertRaises(ValueError) as context:
            self.processor.adjust_image("invalid_adjustment", 1.5)
        self.assertIn("not supported", str(context.exception).lower())
        self.assertIn("adjustment type", str(context.exception).lower())

    def test_brightness_adjustment(self):
        """Test the brightness adjustment"""
        try:
            self.processor.adjust_image(enums.AdjustmentType.BRIGHTNESS.value, 50)
            self.processor.save_image(self.output_path + "/brightened_image_result.jpg")
            self.processor.adjust_image(enums.AdjustmentType.BRIGHTNESS.value, -50)
            self.processor.save_image(self.output_path + "/darkened_image_result.jpg")
        except Exception as e:
            self.fail(f"Adjusting brightness raised an exception {e}")

    def test_contrast_adjustment(self):
        """Test the contrast adjustment"""
        try:
            self.processor.adjust_image(enums.AdjustmentType.CONTRAST.value, 1.5)
            self.processor.save_image(self.output_path + "/high_contrast_image_result.jpg")
            self.processor.adjust_image(enums.AdjustmentType.CONTRAST.value, 0.5)
            self.processor.save_image(self.output_path + "/low_contrast_image_result.jpg")
        except Exception as e:
            self.fail(f"Adjusting contrast raised an exception {e}")

    def test_saturation_adjustment(self):
        """Test the saturation adjustment"""
        try:
            self.processor.adjust_image(enums.AdjustmentType.SATURATION.value, 1.5)
            self.processor.save_image(self.output_path + "/saturated_image_result.jpg")
            self.processor.adjust_image(enums.AdjustmentType.SATURATION.value, 0.5)
            self.processor.save_image(self.output_path + "/desaturated_image_result.jpg")
        except Exception as e:
            self.fail(f"Adjusting saturation raised an exception {e}")

    def test_save_image(self):
        """Test image saving functionality"""
        try:
            # Assume we're saving to a test directory, ensure this directory exists
            self.processor.save_image(
                "/Users/srashkovits/PycharmProjects/onboarding-to-lightricks/output"
                "/filtered_image_result.jpg"
            )
        except IOError as e:
            self.fail(f"Saving image raised an exception {e}")

    def test_save_image_failure(self):
        """Test that saving an image to a non-existent directory raises an IOError"""
        with self.assertRaises(IOError) as context:
            self.processor.save_image("path/to/nonexistent/directory/image.jpg")
        self.assertIn("unable to save image: ", str(context.exception).lower())
