"""Configuration options for the program"""

import importlib.resources as pkg_resources

from rpa_exercise_pyautogui import images

CANVAS_EXECUTABLE: str = 'mspaint'
CONFIDENCE: float = 0.9            # x*100 %
SQUARE_SIDE_LENGTH: int = 100      # pixels
WINDOW_DEFAULT_HEIGHT: int = 1200  # pixels
WINDOW_DEFAULT_WIDTH: int = 1800   # pixels
WINDOW_TITLE: str = "Paint"

with pkg_resources.as_file(pkg_resources.files(images)) as images_dir:
    IMAGES = images_dir

BOTTOM_RIGHT_PNG = IMAGES / 'bottomright.png'
TOP_LEFT_PNG = IMAGES / 'topleft.png'
SQUARE_SCREENSHOT = IMAGES / 'square.png'
