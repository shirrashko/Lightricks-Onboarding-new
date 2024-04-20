import unittest
from unittest.mock import patch
from source.cli import CommandLineInterface


class TestCommandLineInterface(unittest.TestCase):
    @patch('source.cli.ImageProcessor')
    def test_cli_parser_with_valid_args(self, mock_processor):
        test_args = [
            "--image", "path/to/image.jpg",
            "--filter", "blur",
            "--strength", "2"
        ]
        with patch('sys.argv', ["cli.py"] + test_args):
            cli = CommandLineInterface()
            cli.run()

        # Check if ImageProcessor was called with the correct image path
        mock_processor.assert_called_once_with("path/to/image.jpg")
        # Check if filter and strength were handled correctly
        mock_processor_instance = mock_processor.return_value
        mock_processor_instance.apply_filter.assert_called_once_with("blur", 2)