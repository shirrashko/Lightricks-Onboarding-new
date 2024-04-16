import argparse
from image_processor import ImageProcessor


class CommandLineInterface:
    def __init__(self):
        self.parser = self.setup_parser()
        self.processed_image = None

    @staticmethod
    def setup_parser():
        parser = argparse.ArgumentParser(description="Advanced Image Editing CLI Tool")
        parser.add_argument("--image", required=True, help="Path to the image file")
        parser.add_argument("--filter", help="Apply a filter")
        parser.add_argument("--adjust", action='append', nargs=2, help="Adjust image properties")
        parser.add_argument("--save", help="Path to save the edited image")
        parser.add_argument("--display", action='store_true', help="Display the edited image")
        return parser

    def run(self):
        args = self.parser.parse_args()
        processor = ImageProcessor(args.image)

        if args.filter:
            processor.apply_filter(args.filter)

        # if args.adjust:
        #     for adj, value in args.adjust:
        #         processor.adjust_image(adj, int(value))

        if args.save:
            processor.save_image(args.save)
        if args.display:
            processor.display_image()
