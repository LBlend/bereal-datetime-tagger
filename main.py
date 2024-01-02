import argparse
import json
import os
import sys
from datetime import datetime

import dateutil.parser
import exif
import pytz
from PIL import Image


def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="Yeet")
    parser.add_argument(
        "-i", "--input_directory", help="The root folder of your BeReal data"
    )
    parser.add_argument(
        "-o", "--output_directory", help="The folder to export your tagged files to"
    )
    parser.add_argument(
        "-t",
        "--timezone",
        help="The timezone in in which images should be tagged. Defaults to UTC",
        required=False,
    )

    argument = parser.parse_args()
    input_directory = argument.input_directory
    output_directory = argument.output_directory

    if not argument.timezone:
        timezone = pytz.utc
        print("No timezone provided! Using UTC time...")
    else:
        try:
            timezone = pytz.timezone(argument.timezone)
        except pytz.exceptions.UnknonTimeZoneError:
            print("Invalid timezone")
            sys.exit(1)

    # Check if input directory exists
    print("Reading metadata...")
    try:
        with open(f"{input_directory}/memories.json", "r") as f:
            memories = json.load(f)
    except FileNotFoundError:
        print(
            "The provided input directory does not contain a memories.json metadata file"
        )
        sys.exit(1)
    except json.JSONDecodeError:
        print("Failed to read memories.json metadata file.")
        sys.exit(1)

    # Create output directory
    os.makedirs(output_directory, exist_ok=True)

    # Process bereals
    for memory in memories:
        front_image = correct_path(memory["frontImage"]["path"], input_directory)
        print(f"Processing {front_image}")
        front_image = convert_to_jpg(front_image, output_directory)
        set_metadata(front_image, memory["takenTime"], timezone)

        back_image = correct_path(memory["backImage"]["path"], input_directory)
        print(f"Processing {back_image}")
        back_image = convert_to_jpg(back_image, output_directory)
        set_metadata(back_image, memory["takenTime"], timezone)

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


def set_metadata(image_path: str, date: str, timezone):
    date = dateutil.parser.parse(date)
    date = date.astimezone(timezone).strftime("%Y:%m:%d %H:%M:%S")

    with open(image_path, "rb") as image_file:
        my_image = exif.Image(image_file)
        my_image.datetime_original = date

    with open(image_path, "wb") as f:
        f.write(my_image.get_file())


if __name__ == "__main__":
    main()
