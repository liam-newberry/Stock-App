# File created by: Liam Newberry
import os
# m
WIDTH = 1600
HEIGHT = 900
FPS = 45
# Folders
MAIN_FOLDER = os.path.dirname(__file__)
IMAGE_FOLDER = os.path.join(MAIN_FOLDER,"Images")
CURRENT_PATH = os.getcwd()
TEXT_FILE_FOLDER_PATH = CURRENT_PATH + "\Text Files"
# Strings
APP_NAME = "Stock Sphere"
MAX_TICKER_LENGTH_MESSAGE = "Tickers can only be 5 letters long"
MIN_TICKER_LENGTH_MESSAGE = "Tickers must be at leats 1 character"
INVALID_CHAR_MESSAGE = "Invalid character"
# Main settings
LOGO_SCALE = 0.35
# Specific colors
PRIMARY_COLOR = (10,10,40)
SECONDARY_COLOR = (70,237,50)
LIST_COLOR = (50,50,50)
SEARCH_BAR_BACKGROUND_TEXT_COLOR = (230,230,230)
# Object settings
CURSOR_WIDTH = 4
CURSOR_BLINK_INTERVAL = 600
ERROR_MESSAGE_TIME = 1500
FONT = "ariel"
# Common colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)