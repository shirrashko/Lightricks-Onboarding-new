import argparse
import sys
from image_processor import ImageProcessor


class CommandLineInterface:
    """
    Provides a command-line interface for an advanced image editing tool, allowing users to apply
    filters and adjustments to an image and either save or display the result.
    """

    def __init__(self):
        """
        Initializes the command-line parser with all the expected options and their configurations.
        """
        self.parser = CommandLineInterface._setup_parser()

    def run(self):
        """
        Executes the CLI tool by parsing arguments and invoking image processing actions.

        Raises:
            SystemExit: Exits the program if an error occurs during image processing.
        """
        args = self.parser.parse_args()
        try:
            processor = ImageProcessor(args.image)
            CommandLineInterface._handle_filters(processor, args)
            CommandLineInterface._handle_adjustments(processor, args)
            CommandLineInterface._handle_output(processor, args)
        except IOError as e:
            print(f"Error loading or processing image: {e}")
            sys.exit(1)
        except ValueError as e:
            print(f"Error in processing inputs: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error occurred: {e}")
            sys.exit(1)

    @staticmethod
    def _setup_parser() -> argparse.ArgumentParser:
        """
        Sets up and configures the argument parser with options for the image editing tool.

        Returns:
            argparse.ArgumentParser: The configured parser with all the image editing options.
        """
        parser = argparse.ArgumentParser(description="Advanced Image Editing CLI Tool")
        parser.add_argument("--image", required=True, help="Path to the image file")
        parser.add_argument("--filter", action='append', help="Apply a filter e.g., --filter blur")
        parser.add_argument("--adjust", action='append', nargs=2, metavar=('ADJUSTMENT', 'VALUE'),
                            help="Adjust image properties e.g., --adjust brightness 1.5")
        parser.add_argument("--save", help="Path to save the edited image")
        parser.add_argument("--display", action='store_true', help="Display the edited image")
        parser.add_argument("--strength", type=float, default=1.0, help="Strength of the filter")
        return parser

    @staticmethod
    def _handle_filters(processor, args):
        """
        Applies specified filters to the image using the provided strength.

        Parameters:
            processor (ImageProcessor): The processor to apply filters.
            args (Namespace): Command line arguments containing filters and strength.

        Raises:
            SystemExit: Exits the program if an invalid filter name is provided.
        """
        if args.filter:
            for filter_name in args.filter:
                try:
                    processor.apply_filter(filter_name, args.strength)
                except ValueError as e:
                    print(f"Error applying filter: {e}")
                    sys.exit(1)

    @staticmethod
    def _handle_adjustments(processor, args):
        """
        Adjusts image properties as specified by the user.

        Parameters:
            processor (ImageProcessor): The processor to apply adjustments.
            args (Namespace): Command line arguments containing adjustments and their values.

        Raises:
            SystemExit: Exits the program if an invalid adjustment is provided.
        """
        if args.adjust:
            for adjustment, value in args.adjust:
                try:
                    processor.adjust_image(adjustment, float(value))
                except ValueError as e:
                    print(f"Error adjusting image: {e}")
                    sys.exit(1)

    @staticmethod
    def _handle_output(processor, args):
        """
        Handles the output of the processed image, saving or displaying it as specified.
        """
        if args.save:
            try:
                processor.save_image(args.save)
                print(f"Image successfully saved to {args.save}")
            except IOError as e:
                print(f"Error saving image: {e}")
                sys.exit(1)
        if args.display:
            try:
                processor.display_image()
                print("Image displayed successfully.")
            except Exception as e:  # Catching a general exception if display fails
                print(f"Error displaying image: {e}")
                sys.exit(1)
