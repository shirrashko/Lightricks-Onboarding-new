import numpy as np
from PIL import Image
from custom_image import CustomImage


class BaseFilter:
    """
    Abstract base class for image filters.
    """

    def apply(self, image: CustomImage) -> CustomImage:
        """
        Apply the filter to the given image.

        Args:
            image (CustomImage): The PIL Image to be processed.

        Returns:
            CustomImage: The processed image.

        Raises:
            NotImplementedError: If the method is not overridden in the derived class.
        """
        raise NotImplementedError("Each filter must implement the apply method.")

    @staticmethod
    def convolve(image_array: np.ndarray, kernel: np.ndarray) -> np.ndarray:
        """
        Perform convolution on the given image array using the specified kernel.
        """
        if image_array.ndim == 2:  # If grayscale, add a third dimension
            image_array = image_array[:, :, np.newaxis]

        kernel_height, kernel_width = kernel.shape
        pad_height, pad_width = kernel_height // 2, kernel_width // 2
        padded_image = np.pad(image_array, [(pad_height, pad_height), (pad_width, pad_width), (0, 0)],
                              mode='constant', constant_values=0)

        output_array = np.zeros_like(image_array)
        for i in range(image_array.shape[0]):
            for j in range(image_array.shape[1]):
                for k in range(image_array.shape[2]):
                    region = padded_image[i:i + kernel_height, j:j + kernel_width, k]
                    output_array[i, j, k] = np.sum(region * kernel)

        if output_array.shape[2] == 1:  # If originally grayscale, remove the third dimension
            output_array = output_array[:, :, 0]
        return output_array


class BlurFilter(BaseFilter):
    """
    Applies a simple averaging blur filter to an image.
    """

    def apply(self, custom_image: CustomImage) -> None:
        image_array = np.array(custom_image.convert_to_rgb().get_image(), dtype=np.float32)
        kernel = np.ones((3, 3)) / 9  # Define a 3x3 averaging kernel
        blurred_array = self.convolve(image_array, kernel)
        blurred_image = Image.fromarray(blurred_array.astype('uint8'))
        custom_image.set_image(blurred_image)  # Update the CustomImage with the blurred image


class EdgeDetectionFilter(BaseFilter):
    """
    Applies an edge detection filter using the Sobel operator to an image.
    """

    def apply(self, custom_image: CustomImage) -> None:
        image_array = np.array(custom_image.convert_to_grayscale().get_image(), dtype=np.float32)
        sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
        sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
        edges_x = self.convolve(image_array, sobel_x)
        edges_y = self.convolve(image_array, sobel_y)
        combined_edges = np.hypot(edges_x, edges_y)
        edge_image = Image.fromarray(np.clip(combined_edges, 0, 255).astype('uint8'))
        custom_image.set_image(edge_image)  # Update the CustomImage with the edge-detected image


class SharpenFilter(BaseFilter):
    """
    Applies a sharpening filter to enhance the edges in an image.
    """

    def apply(self, custom_image: CustomImage) -> None:
        image_array = np.array(custom_image.convert_to_rgb().get_image(), dtype=np.float32)
        sharpen_kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        sharpened_array = self.convolve(image_array, sharpen_kernel)
        sharpened_image = Image.fromarray(np.clip(sharpened_array, 0, 255).astype('uint8'))
        custom_image.set_image(sharpened_image)  # Update the CustomImage with the sharpened image

