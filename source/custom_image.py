from PIL import Image


class CustomImage:
    """
    CustomImage provides a wrapper around the PIL Image library, encapsulating common image
    operations for ease of use in other parts of an application.
    """

    MAX_INTENSITY = 255
    MIN_INTENSITY = 0

    def __init__(self, path: str):
        """
        Initializes a new instance of CustomImage by loading an image from a specified file path.
        """
        try:
            with Image.open(path) as img:
                self.image = img.copy()  # Make a copy of the image to work with
        except IOError as e:
            raise IOError(f"Unable to open image: {e}") from e

    def save(self, path: str) -> None:
        """
        Saves the current image to a specified file path.

        Args:
            path (str): The file path where the image will be saved.

        Raises:
            IOError: If the image cannot be saved, possibly due to an unsupported format or permissions issue.
        """
        try:
            self.image.save(path)
        except IOError as e:
            raise IOError(f"Unable to save image: {e}") from e

    def get_image(self) -> Image.Image:
        """
        Returns the current PIL Image object.

        Returns:
            Image.Image: The current PIL Image object.
        """
        return self.image

    def set_image(self, image: Image.Image) -> None:
        """
        Sets the image of this CustomImage instance to a new PIL Image object and updates related properties.

        Args:
            image (Image.Image): A new PIL Image object to replace the current image.
        """
        self.image = image

    def show(self) -> None:
        """
        Displays the current image using the default image viewer.
        """
        self.image.show()

    def convert_to_grayscale(self) -> "CustomImage":
        """
        Converts the image to grayscale.

        Returns:
            CustomImage: The current instance with the updated image.
        """
        self.image = self.image.convert("L")
        return self

    def convert_to_rgb(self) -> "CustomImage":
        """
        Converts the image to RGB mode.

        Returns:
            CustomImage: The current instance with the updated image.
        """
        self.image = self.image.convert("RGB")
        return self
