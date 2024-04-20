import numpy as np
from PIL import Image
from custom_image import CustomImage


class BaseFilter:
    """
    Abstract base class for image filters. This class provides a framework for implementing various
    image filtering techniques.

    Subclasses should implement the `apply` method to define specific filter behavior.
    """

    def apply(self, image: CustomImage) -> None:
        """
        Apply the filter to the given image. This method should be overridden in subclass.

        Args:
            image (CustomImage): The image to be processed, wrapped in a CustomImage instance.

        Returns:
            None

        Raises:
            NotImplementedError: If the method is not implemented in the subclass.
        """
        raise NotImplementedError("Each filter must implement the apply method.")

    @staticmethod
    def convolve(image_array: np.ndarray, kernel: np.ndarray) -> np.ndarray:
        """
        Perform convolution on the given image array using the specified kernel.

        Args:
            image_array (np.ndarray): The input image as a 2D (grayscale) or 3D (color) numpy array.
            kernel (np.ndarray): The convolution kernel as a 2D numpy array.

        Returns:
            np.ndarray: The convolved image as a numpy array. The output will match the input dimensions.

        Raises:
            ValueError: If the kernel dimensions are greater than the image dimensions.
        """
        # Ensure the image is at least 3D (handle grayscale images by adding a channel dimension).
        if image_array.ndim == 2:
            image_array = image_array[:, :, np.newaxis]

        kernel_height, kernel_width = kernel.shape
        if kernel_height > image_array.shape[0] or kernel_width > image_array.shape[1]:
            raise ValueError("Kernel size cannot be greater than image dimensions.")

        pad_height, pad_width = kernel_height // 2, kernel_width // 2

        # Pads with the reflection of the vector mirrored on the first and last values of the vector along each axis.
        # For example, padding [1,2,3,4,5] with 2 elements on each side will result in [3,2,1,2,3,4,5,4,3].
        padded_image = np.pad(
            image_array, ((pad_height, pad_height), (pad_width, pad_width), (0, 0)), mode="reflect"
        )

        # Prepare an output array of the same shape as the input.
        output_array = np.zeros_like(image_array)

        # Perform convolution operation.
        for i in range(image_array.shape[0]):
            for j in range(image_array.shape[1]):
                for k in range(image_array.shape[2]):  # Handle each channel independently.
                    region = padded_image[i: i + kernel_height, j: j + kernel_width, k]
                    output_array[i, j, k] = np.sum(region * kernel)

        # If the original image was grayscale (single channel), remove the singleton dimension.
        if output_array.shape[2] == 1:
            output_array = output_array.squeeze(axis=2)

        return output_array


class BlurFilter(BaseFilter):
    """
    Applies a simple averaging blur filter to an image.
    """

    def apply(self, custom_image: CustomImage) -> None:
        """
        Applies a blur filter to the given CustomImage instance using a simple averaging kernel.

        Args:
            custom_image (CustomImage): The image to apply the blur filter to.

        Returns:
            None
        """
        image_array = np.array(custom_image.convert_to_rgb().get_image(), dtype=np.float32)
        kernel = np.ones((3, 3)) / 9  # Define a 3x3 averaging kernel
        blurred_array = self.convolve(image_array, kernel)
        blurred_image = Image.fromarray(blurred_array.astype("uint8"))
        custom_image.set_image(blurred_image)  # Update the CustomImage with the blurred image


class EdgeDetectionFilter(BaseFilter):
    """
    Applies an edge detection filter using the Sobel operator to an image. This filter highlights edges in the image.
    """

    def apply(self, custom_image: CustomImage) -> None:
        """
        Applies an edge detection filter to the given CustomImage instance using the Sobel operator.

        Args:
            custom_image (CustomImage): The image to apply the edge detection filter to.

        Returns:
            None
        """
        image_array = np.array(custom_image.convert_to_grayscale().get_image(), dtype=np.float32)
        sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
        sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
        edges_x = self.convolve(image_array, sobel_x)
        edges_y = self.convolve(image_array, sobel_y)
        combined_edges = np.hypot(edges_x, edges_y)
        edge_image = Image.fromarray(
            np.clip(combined_edges, CustomImage.MIN_INTENSITY, CustomImage.MAX_INTENSITY).astype("uint8")
        )
        custom_image.set_image(edge_image)  # Update the CustomImage with the edge-detected image


class SharpenFilter(BaseFilter):
    """
    Applies a sharpening filter to enhance the edges in an image.
    """

    def apply(self, custom_image: CustomImage) -> None:
        """
        Applies a sharpening filter to the given CustomImage instance to enhance image clarity.

        Args:
            custom_image (CustomImage): The image to apply the sharpening filter to.

        Returns:
            None
        """
        image_array = np.array(custom_image.convert_to_rgb().get_image(), dtype=np.float32)
        sharpen_kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        sharpened_array = self.convolve(image_array, sharpen_kernel)
        sharpened_image = Image.fromarray(
            np.clip(sharpened_array, CustomImage.MIN_INTENSITY, CustomImage.MAX_INTENSITY).astype("uint8")
        )
        custom_image.set_image(sharpened_image)  # Update the CustomImage with the sharpened image
