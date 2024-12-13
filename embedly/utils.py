import base64
from PIL import Image  # Pillow library for image handling
import io
from dash import Dash, dcc, html, Input, Output, no_update, callback
import plotly.graph_objects as go
import pandas as pd
import cv2
import os

## requirements.txt file should include the following:
'''
dash
plotly
pandas
opencv-python-headless

'''


def list_files(path: str) -> list:
    """
    Lists all files in a directory. Also removes .DS_Store if present, which is helpful when working with images
    Input: str
    Returns: list
    """
    files = os.listdir(path)
    if ".DS_Store" in files:
        files.remove(".DS_Store")
    return files


def quick_dir(path: str, folder_name: str) -> str:
    """
    Checks if a directory exists. If not, creates it. Returns the final path
    Input: str, str
    Returns: str
    """

    # check if path ends with "/"
    if path[-1] != "/":
        path = path + "/"

    # check if the folder exists
    if not os.path.exists(path + folder_name):
        os.makedirs(path + folder_name, exist_ok=True)

    return path + folder_name + "/"

def create_thumbnail(input_image_path, output_image_path, max_size=256, chan_to_save=None, enhance_contrast=False):
    """
    Create a thumbnail of the image at `input_image_path` and save it to `output_image_path`.

    :param input_image_path: Path to the original image.
    :param output_image_path: Path to save the thumbnail.
    :param max_size: Maximum size of the thumbnail (width or height). If the image is smaller than this, it will not be resized. Keep the aspect ratio.
    """
    # Read the image
    image = cv2.imread(input_image_path, cv2.IMREAD_UNCHANGED)  # Load with all channels, including alpha
    
    if image is None:
        raise FileNotFoundError(f"Image not found: {input_image_path}")
    

    # check to see if it's single channel or not
    if len(image.shape) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    else:
        # Convert the image to RGB (OpenCV uses BGR as default) but check if dims are (h, w, c) or (c, h, w)
        if image.shape[0] < 4:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        else:
            image = cv2.cvtColor(image.transpose(1, 2, 0), cv2.COLOR_BGR2RGB)
    
    # If a specific channel is requested, keep only that channel
    h, w = image.shape[:2]

    if chan_to_save is not None:
        image = image[:, :, chan_to_save]
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    # keep the aspect ratio, resize the bigger dimension to size if bigger than max_size
    if h > max_size or w > max_size:
        if h > w:
            new_h = max_size
            new_w = int(w * (max_size / h))
        else:
            new_w = max_size
            new_h = int(h * (max_size / w))
        image = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
    if enhance_contrast:
        image = cv2.convertScaleAbs(image, alpha=1.5, beta=0)
    # Resize the image
    #image = cv2.resize(image, size, interpolation=cv2.INTER_AREA)

    # Save the thumbnail
    cv2.imwrite(output_image_path, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    
     
def encode_image_to_base64(image_path):


    """
    Encode a local image file (including TIFF) as a base64 string.

    :param image_path: Path to the image file.
    :return: Base64-encoded image string.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    # check if the image is a TIFF


    buffer = io.BytesIO()
    img = Image.open(image_path)
    img.save(buffer, format="jpeg")
    return 'data:image/jpeg;base64,' + base64.b64encode(buffer.getvalue()).decode()
#base64.b64encode(buffer.getvalue()).decode()


#