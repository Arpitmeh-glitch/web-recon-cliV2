import os
from datetime import datetime


def file_metadata_analyzer():
    print("\n========================")
    print("File Metadata Analyzer")
    print("========================")

    file_path = input("Enter file path: ").strip()

    if not os.path.isfile(file_path):
        print("File not found.")
        return

    try:
        info = os.stat(file_path)

        file_name = os.path.basename(file_path)
        file_size = info.st_size

        modified_time = datetime.fromtimestamp(info.st_mtime)
        accessed_time = datetime.fromtimestamp(info.st_atime)
        changed_time = datetime.fromtimestamp(info.st_ctime)

        print("\n========================")
        print("File Metadata")
        print("========================")

        print(f"File Name:     {file_name}")
        print(f"File Path:     {os.path.abspath(file_path)}")
        print(f"File Size:     {file_size} bytes")
        print(f"Modified Time: {modified_time}")
        print(f"Accessed Time: {accessed_time}")
        print(f"Changed Time:  {changed_time}")

    except Exception as error:
        print(f"Could not analyze file: {error}")