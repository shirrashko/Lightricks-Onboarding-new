import argparse
import sys
from image_processor import ImageProcessor
from source.enums import FilterName
import logging

# Configure logging at the top of your script
logging.basicConfig(
    level=logging.INFO,  # Adjust the level as needed (DEBUG, ERROR, WARNING, etc.)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Example format
    handlers=[
        logging.FileHandler("../image_processor.log"),  # Log messages are saved to this file
        logging.StreamHandler(sys.stdout),  # Log messages are also printed to stdout
    ],
)


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
            self._handle_filters(processor, args)
            self._handle_adjustments(processor, args)
            self._handle_output(processor, args)
        except IOError as e:
            self._output_error_and_exit_program(e, "Error loading or processing image")
        except ValueError as e:
            self._output_error_and_exit_program(e, "Error in processing inputs")
        except Exception as e:
            self._output_error_and_exit_program(e, "Unexpected error occurred")

    @staticmethod
    def _setup_parser() -> argparse.ArgumentParser:
        """
        Sets up and configures the argument parser with options for the image editing tool.

        Returns:
            argparse.ArgumentParser: The configured parser with all the image editing options.
        """
        parser = argparse.ArgumentParser(description="Advanced Image Editing CLI Tool")
        parser.add_argument("--image", required=True, help="Path to the image file")
        parser.add_argument(
            "--filter",
            action="append",
            choices=[f.value for f in FilterName],
            help="Apply a filter e.g., --filter blur",
        )
        parser.add_argument(
            "--adjust",
            action="append",
            nargs=2,
            metavar=("ADJUSTMENT", "VALUE"),
            help="Adjust image properties e.g., --adjust brightness 1.5",
        )
        parser.add_argument("--save", help="Path to save the edited image")
        parser.add_argument("--display", action="store_true", help="Display the edited image")
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
        try:
            if args.filter:
                for filter_name in args.filter:
                    processor.apply_filter(filter_name, args.strength)
        except ValueError as e:
            CommandLineInterface._output_error_and_exit_program(e, "Error applying filter")

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
        try:
            if args.adjust:
                for adjustment_pair in args.adjust:
                    adjustment, value = adjustment_pair
                    processor.adjust_image(adjustment, float(value))
        except ValueError as e:
            CommandLineInterface._output_error_and_exit_program(e, "Error adjusting image")

    @staticmethod
    def _handle_output(processor, args):
        """
        Handles the output of the processed image, saving or displaying it as specified.
        """
        if args.save:
            try:
                processor.save_image(args.save)
                logging.info(f"Image successfully saved to {args.save}")
            except IOError as e:
                CommandLineInterface._output_error_and_exit_program(e, "Error saving image")
        if args.display:
            try:
                processor.display_image()
                logging.info("Image displayed successfully.")
            except Exception as e:
                CommandLineInterface._output_error_and_exit_program(e, "Error displaying image")

    @staticmethod
    def _output_error_and_exit_program(error, prefix_message="Error"):
        """
        Outputs an error message and exits the program.

        Args:
            error (Exception): The exception object containing the error message.
            prefix_message (str): A prefix label for the error message to provide context.
        """
        logging.error(f"{prefix_message}: {error}")
        sys.exit(1)
