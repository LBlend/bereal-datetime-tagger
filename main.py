import json
import os
import sys
from datetime import datetime

import dateutil
import exif
from PIL import Image


def main():
    # Parse command line arguments
    # I should probably use a lib to do flags but whatever
    sys.argv = sys.argv[1:]
    if len(sys.argv) != 2 or len(sys.argv) != 3:
        print("Usage: python main.py <input_directory> <output_directory>")
        sys.exit(1)

    input_directory = sys.argv[0]
    output_directory = sys.argv[1]

    # Check if input directory exists
    print("Reading metadata...")
    with open(f"{input_directory}/memories.json", "r") as f:
        memories = json.load(f)

    # Create output directory
    os.makedirs(output_directory, exist_ok=True)

    for memory in memories:
        front_image = correct_path(memory["frontImage"]["path"], input_directory)
        print(f"Processing {front_image}")
        front_image = convert_to_jpg(front_image, output_directory)
        set_metadata(front_image, memory["takenTime"])

        back_image = correct_path(memory["backImage"]["path"], input_directory)
        print(f"Processing {back_image}")
        back_image = convert_to_jpg(back_image, output_directory)
        set_metadata(back_image, memory["takenTime"])

    print("Done!")


def convert_to_jpg(image_path: str, output_directory: str) -> str:
    image = Image.open(image_path)
    image = image.convert("RGB")

    file_name = get_filename(image_path)
    new_path = f"{output_directory}/{file_name}.jpg"

    image.save(new_path)
    return new_path


def correct_path(path: str, input_directory: str) -> str:
    input_directory = input_directory.replace("\\", "/")  # Fuck windows
    input_directory = (
        input_directory[:-1] if input_directory[-1] == "/" else input_directory
    )
    path = path.split("/")
    path[0] = input_directory
    path.pop(2)
    return "/".join(path)


def get_filename(path: str) -> str:
    return path.split("/")[-1].split(".")[0]


def set_metadata(image_path: str, date: str):
    date = dateutil.parser.parse(date).strftime("%Y:%m:%d %H:%M:%S")

    with open(image_path, "rb") as image_file:
        my_image = exif.Image(image_file)
        my_image.datetime_original = date

    with open(image_path, "wb") as f:
        f.write(my_image.get_file())


if __name__ == "__main__":
    main()
