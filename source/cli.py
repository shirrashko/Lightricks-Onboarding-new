import argparse
from image_processor import ImageProcessor


class CommandLineInterface:
    def __init__(self):
        self.parser = self.setup_parser()

    @staticmethod
    def setup_parser():
        parser = argparse.ArgumentParser(description="Advanced Image Editing CLI Tool")
        parser.add_argument("--image", required=True, help="Path to the image file")
        parser.add_argument("--filter", action='append', help="Apply a filter e.g., --filter blur")
        parser.add_argument("--adjust", action='append', nargs=2, metavar=('ADJUSTMENT', 'VALUE'),
                            help="Adjust image properties e.g., --adjust brightness 1.5")
        parser.add_argument("--save", help="Path to save the edited image")
        parser.add_argument("--display", action='store_true', help="Display the edited image")
        return parser

    def run(self):
        args = self.parser.parse_args()
        processor = ImageProcessor(args.image)

        # Process each filter in the order they were provided
        if args.filter:
            for filter_name in args.filter:
                processor.apply_filter(filter_name)

        # Process each adjustment in the order they were provided
        if args.adjust:
            for adjustment, value in args.adjust:
                processor.adjust_image(adjustment, float(value))

        # Save or display the image according to the provided options
        if args.save:
            processor.save_image(args.save)
        if args.display:
            processor.display_image()
