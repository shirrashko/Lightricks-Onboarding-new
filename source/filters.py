from PIL import Image
import numpy as np


class BaseFilter:
    def apply(self, image):
        raise NotImplementedError("Each filter must implement the apply method.")


class BlurFilter(BaseFilter):
    def apply(self, custom_image):
        # Ensure the image is in an editable format
        image = custom_image.image.convert("RGB")
        # Get dimensions
        width, height = image.size

        # Prepare a new image for output
        blurred_image = Image.new("RGB", (width, height))
        pixels = image.load()
        output_pixels = blurred_image.load()

        # Iterate over every pixel except the border
        for i in range(1, width - 1):
            for j in range(1, height - 1):
                # Initialize the sum for each color channel
                total_red, total_green, total_blue = 0, 0, 0

                # Sum up all the pixel values in the 3x3 neighborhood
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        r, g, b = pixels[i + dx, j + dy]
                        total_red += r
                        total_green += g
                        total_blue += b

                # Calculate the average for each color channel
                avg_red = total_red // 9
                avg_green = total_green // 9
                avg_blue = total_blue // 9

                # Set the pixel to the average value
                output_pixels[i, j] = (avg_red, avg_green, avg_blue)

        return blurred_image


class EdgeDetectionFilter(BaseFilter):
    def apply(self, custom_image):
        # Convert to grayscale
        image_array = np.array(custom_image.image.convert("L"))

        sobel_x_kernel = np.array([[-1, 0, 1],
                                   [-2, 0, 2],
                                   [-1, 0, 1]])

        sobel_y_kernel = np.array([[-1, -2, -1],
                                   [0, 0, 0],
                                   [1, 2, 1]])

        # Apply the Sobel filter
        edges_x = self.convolve(image_array, sobel_x_kernel)
        edges_y = self.convolve(image_array, sobel_y_kernel)

        # Combine the horizontal and vertical edges
        combined_edges = np.hypot(edges_x, edges_y)
        combined_edges = (combined_edges / combined_edges.max() * 255).astype(np.uint8)

        # Convert back to PIL Image and return
        return Image.fromarray(combined_edges)

    def convolve(self, image_array, kernel):
        # This function will perform the convolution operation (without padding)
        kernel_size = kernel.shape[0]
        kernel_radius = kernel_size // 2
        image_height, image_width = image_array.shape
        result = np.zeros((image_height - kernel_size + 1, image_width - kernel_size + 1))

        for i in range(kernel_radius, image_height - kernel_radius):
            for j in range(kernel_radius, image_width - kernel_radius):
                region = image_array[i - kernel_radius:i + kernel_radius + 1, j - kernel_radius:j + kernel_radius + 1]
                result[i - kernel_radius, j - kernel_radius] = np.sum(region * kernel)

        return result


class SharpenFilter(BaseFilter):
    def apply(self, custom_image):
        # Convert the image to a numpy array for manipulation
        image_array = np.array(custom_image.image.convert("RGB"))
        original_array = image_array.copy()

        # Define the sharpening kernel, it accentuates the current pixel and subtracts some of the surrounding pixel
        # values
        sharpen_kernel = np.array([
            [-1, -1, -1],
            [-1,  9, -1],
            [-1, -1, -1]
        ])

        # Apply the convolution operation (this is a simplistic and not optimized way to apply a kernel to an image)
        padded_image = np.pad(image_array, [(1, 1), (1, 1), (0, 0)], mode='constant', constant_values=0)
        for i in range(image_array.shape[0]):
            for j in range(image_array.shape[1]):
                # Extract the region of interest
                region = padded_image[i:i+3, j:j+3]
                # Apply the kernel to each channel
                for k in range(3):  # Assuming RGB
                    image_array[i, j, k] = np.clip(np.sum(region[:, :, k] * sharpen_kernel), 0, 255)

        # The sharpened image is now a combination of the original and the high-pass filter result
        sharpened_array = np.clip(original_array + (image_array - original_array), 0, 255).astype(np.uint8)

        # Convert the result back to an image
        return Image.fromarray(sharpened_array)
