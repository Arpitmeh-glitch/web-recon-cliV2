import os


# Common file signatures (magic bytes)
SIGNATURES = {
    b"\xFF\xD8\xFF": "JPEG Image",
    b"\x89PNG\r\n\x1a\n": "PNG Image",
    b"%PDF": "PDF Document",
    b"PK\x03\x04": "ZIP Archive / Office Document",
    b"\x7fELF": "ELF Executable",
    b"MZ": "Windows Executable",
    b"GIF87a": "GIF Image",
    b"GIF89a": "GIF Image",
}


def detect_file_type(file_path):
    try:
        with open(file_path, "rb") as file:
            header = file.read(16)

        for signature, file_type in SIGNATURES.items():
            if header.startswith(signature):
                return file_type

        return "Unknown"

    except Exception:
        return None


def file_signature_checker():
    print("\n========================")
    print("File Signature Checker")
    print("========================")

    file_path = input("Enter file path: ").strip()

    if not os.path.isfile(file_path):
        print("File not found.")
        return

    detected_type = detect_file_type(file_path)

    if detected_type is None:
        print("Could not read file.")
        return

    extension = os.path.splitext(file_path)[1].lower()

    print("\n========================")
    print("Signature Results")
    print("========================")

    print(f"File:          {os.path.basename(file_path)}")
    print(f"Extension:     {extension if extension else 'None'}")
    print(f"Detected Type: {detected_type}")