"""
A script to replace white(-ish) pixels in a picture with transparent pixels.
The result image will be saved as a png-file.
Simple drag and drop the image(s) onto the script file.
The new image will be saved in the same folder as the starting image.
The new image will be named transparent-originalname-percentage.png
"""

import os
import sys

from PIL import Image

def make_savename(filepath, percentage):
    """
    Adds "transparent-" before the file name and the white percentage
    that has been removed after the file name and returns the string.
    Will work even if the filename contains periods.

    :Args:
    `filepath` is the full path of the image to resize
    `percentage` is the white percentage to be replaced with transparency

    :Returns:
    The new properly formatted string.
    """
    filepath = filepath.split(os.sep)
    filename = filepath[-1].split(".") # Split into list, so we can pop off last element
    filename.pop() # Removes last element(extension)
    filename = ".".join(filename) # Must be done like this in case filename has a period in it
    filename = "transparent-" + filename + "-" + str(percentage) + ".png"
    filepath[-1] = filename
    filepath = os.sep.join(filepath)
    return filepath

def replace_white(filepath, percentage):
    try:
        img = Image.open(filepath)
    except OSError:
        print(filepath + " is not a valid file format.")
        input("Press enter to continue script")
        return
    except Exception as exc:
        print(exc)
        input("Something went wrong when opening image. Press enter to continue script")
        return

    rgb_value = round(percentage / 100 * 255)
    img = img.convert("RGBA")
    data = img.getdata()

    new_data = list()
    for item in data:
        if item[0] >= rgb_value and item[1] >= rgb_value and item[2] >= rgb_value:
            new_data.append((0, 0, 0, 0))
        else:
            new_data.append(item)

    img.putdata(new_data)
    return img

def run(argv):
    """
    Main function
    """
    percentage = input("White percentage to be replaced: ")
    try:
        percentage = int(percentage)
    except ValueError:
        print("You must enter an integer 1-100.")
        input("Press enter to exit script")
        return
    if len(argv) > 1:
        argv.pop(0)
        for filepath in argv:
            img = replace_white(filepath, percentage)
            img.save(make_savename(filepath, percentage))
            print("Image edited and saved...", flush=True)
        print("All images edited and saved. Exiting script...", flush=True)
    else:
        print("Drag and drop the image(s) to be resized on top of this file.")

if __name__ == "__main__":
    run(sys.argv)
