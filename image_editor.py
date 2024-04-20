from source.cli import CommandLineInterface

if __name__ == "__main__":
    """
    Entry point for the command-line application. This script initializes and runs the command-line interface
    for the advanced image editing tool.

    The CLI provides a range of options to apply filters, adjust image properties, save images, and display images
    through terminal commands. Users can specify the path to an image file, choose filters and adjustments, and
    opt to save or display the processed image.

    Usage:
        python image_editor.py --image <path_to_image> --filter blur --strength 2 --save <path_to_save>
    """
    cli = CommandLineInterface()
    cli.run()
