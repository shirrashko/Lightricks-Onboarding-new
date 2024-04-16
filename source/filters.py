from PIL import Image, ImageFilter, ImageOps, ImageChops
import numpy as np


class BaseFilter:
    def apply(self, image):
        raise NotImplementedError("Each filter must implement the apply method.")


class BlurFilter(BaseFilter):
    def apply(self, image):
        # Ensure the image is in an editable format
        image = image.convert("RGB")

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
    def apply(self, image):
        # Using Sobel operator to detect edges
        image = image.convert("L")  # Convert to grayscale
        sobel_x = ImageFilter.Kernel(
            size=(3, 3),
            kernel=(-1, 0, 1, -2, 0, 2, -1, 0, 1),
            scale=1
        )
        sobel_y = ImageFilter.Kernel(
            size=(3, 3),
            kernel=(-1, -2, -1, 0, 0, 0, 1, 2, 1),
            scale=1
        )
        edges_x = image.filter(sobel_x)
        edges_y = image.filter(sobel_y)
        # Combine the horizontal and vertical edges
        combined = ImageChops.add(edges_x, edges_y)
        return combined


class SharpenFilter(BaseFilter):
    def apply(self, image):
        # Applying a sharpening filter that accentuates edges
        kernel = ImageFilter.Kernel(
            size=(3, 3),
            kernel=(-1, -1, -1, -1, 9, -1, -1, -1, -1),
            scale=1
        )
        return image.filter(kernel)
