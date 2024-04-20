from enum import Enum


class FilterName(Enum):
    """
    Enumerates the available filter names.
    """

    BLUR = "blur"
    EDGE_DETECTION = "edge_detection"
    SHARPEN = "sharpen"


class AdjustmentType(Enum):
    """
    Enumerates the types of adjustments that can be made to an image.
    """

    BRIGHTNESS = "brightness"
    CONTRAST = "contrast"
    SATURATION = "saturation"
