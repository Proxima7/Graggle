import base64
import io
from globals import logger

import numpy as np
from imageio.v2 import imread
import cv2
import os


def convert_ndarray_to_base_64(image: np.ndarray):
    '''
    Converts ndarray numpy image to base64 encoded string.

    Args:
        image: ndarray image

    Returns:
        base64 encoded string
    '''
    image_as_array = cv2.imencode('.png', image)[1].tobytes()
    return base64.b64encode(image_as_array).decode()

def convert_base_64_to_ndarray(base64img: str):
    '''
    Converts a Base64 encoded image (as returned by our DB) to a ndarray grayscale image.

    Args:
        base64img: Base64 encoded image
        color: Color of the output image

    Returns:
        ndarray grayscale image
    '''
    if base64img.startswith('data:'):
        encoded_img = base64img.split(',')[1]
    else:
        encoded_img = base64img
    decoded_img = np.array(imread(io.BytesIO(base64.b64decode(encoded_img))))
    swapped = decoded_img[..., [2, 1, 0]].copy()
    return swapped

def check_base64_image(image_base64: str):
    '''
    Checks if the given image is a valid base64 image.

    Args:
        image_base64: Base64 encoded image

    Returns:
        True if the image is valid, False otherwise
    '''
    try:
        assert convert_base_64_to_ndarray(image_base64) is not None
        return True
    except Exception as e:
        logger.info(f"Exception raised in check_base64_image: {e}")
        return False

def average_image_size(images: list):
    no_images = len(images)
    total_size_mb = 0
    for image in images:
        size_mb = image.nbytes / (1024 * 1024)
        total_size_mb = total_size_mb + size_mb
    return total_size_mb / no_images




def create_random_4_3_preview_image(images: list):
    centered_images = []

    # crop center
    for image in images:
        y, x, _ = image.shape
        # define the size of the cropped image
        crop_size = (int(x/2), int(y/2))

        # get the center coordinates of the image

        cx, cy = x // 2, y // 2

        # calculate the bounds of the cropped image
        x1 = cx - crop_size[0] // 2
        y1 = cy - crop_size[1] // 2
        x2 = x1 + crop_size[0]
        y2 = y1 + crop_size[1]

        # crop the image
        cropped_image = image[y1:y2, x1:x2, :]

        centered_images.append(cropped_image)

    # define the size of the output image (400x300)
    output_size = (1280, 960)

    # create a black output image
    preview_image = np.zeros((output_size[1], output_size[0], 3), dtype=np.uint8)

    # loop through the list of images and insert each one into the output image
    for i in range(len(centered_images)):
        x = i % 4
        y = i // 4
        x_start = x * output_size[0] // 4
        y_start = y * output_size[1] // 3
        preview_image[y_start:y_start + output_size[1] // 3, x_start:x_start + output_size[0] // 4] = cv2.resize(
            centered_images[i], (output_size[0] // 4, output_size[1] // 3))

    return preview_image

def object_to_dict(obj):
    if isinstance(obj, (int, float, str)):
        return obj
    elif isinstance(obj, dict):
        return {k: object_to_dict(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [object_to_dict(item) for item in obj]
    else:
        return {k: object_to_dict(v) for k, v in obj.__dict__.items()}


def remove_objects_of_type(data, obj_type):
    if isinstance(data, dict):
        # Iterate over the dictionary keys
        for key in list(data.keys()):
            value = data[key]
            if isinstance(value, obj_type):
                # Remove the object if it matches the specified type
                del data[key]
            else:
                # Recursively call the function for nested dictionaries
                remove_objects_of_type(value, obj_type)
    elif isinstance(data, list):
        # Iterate over the list elements
        for item in data:
            if isinstance(item, obj_type):
                # Remove the object if it matches the specified type
                data.remove(item)
            else:
                # Recursively call the function for nested dictionaries or lists
                remove_objects_of_type(item, obj_type)
