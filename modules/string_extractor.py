import os
import re


def extract_strings(file_path, min_length=4):
    try:
        with open(file_path, "rb") as file:
            data = file.read()

        pattern = rb"[ -~]{" + str(min_length).encode() + rb",}"

        strings = re.findall(pattern, data)

        results = []

        for string in strings:
            text = string.decode(errors="ignore")
            results.append(text)

        return results

    except Exception:
        return None


def string_extractor():
    print("\n========================")
    print("String Extractor")
    print("========================")

    file_path = input("Enter file path: ").strip()

    if not os.path.isfile(file_path):
        print("File not found.")
        return

    strings = extract_strings(file_path)

    if strings is None:
        print("Could not read file.")
        return

    print("\n========================")
    print("Extracted Strings")
    print("========================")

    print(f"File: {os.path.basename(file_path)}")
    print(f"Strings found: {len(strings)}\n")

    if not strings:
        print("No readable strings found.")
        return

    for string in strings:
        print(string)