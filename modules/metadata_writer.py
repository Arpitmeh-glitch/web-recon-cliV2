import os
from PIL import Image


def write_jpeg_metadata(file_path, artist, description):
    try:
        image = Image.open(file_path)

        exif = image.getexif()

        # EXIF tag 315 = Artist
        exif[315] = artist

        # EXIF tag 270 = ImageDescription
        exif[270] = description

        image.save(file_path, exif=exif)

        return True

    except Exception as error:
        print(f"Error: {error}")
        return False


def metadata_writer():
    print("\n========================")
    print("Metadata Writer")
    print("========================")

    file_path = input("Enter JPEG file path: ").strip()

    if not os.path.isfile(file_path):
        print("File not found.")
        return

    extension = os.path.splitext(file_path)[1].lower()

    if extension not in [".jpg", ".jpeg"]:
        print("Currently only JPEG files are supported.")
        return

    print("\nEnter metadata")

    artist = input("Artist: ").strip()
    description = input("Description: ").strip()

    success = write_jpeg_metadata(
        file_path,
        artist,
        description
    )

    if success:
        print("\nMetadata written successfully.")