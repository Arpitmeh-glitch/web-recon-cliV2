import hashlib
import os


def calculate_hash(file_path, algorithm):
    try:
        hash_object = hashlib.new(algorithm)

        with open(file_path, "rb") as file:
            while True:
                chunk = file.read(4096)

                if not chunk:
                    break

                hash_object.update(chunk)

        return hash_object.hexdigest()

    except Exception:
        return None


def file_hash_analyzer():
    print("\n========================")
    print("File Hash Analyzer")
    print("========================")

    file_path = input("Enter file path: ").strip()

    if not os.path.isfile(file_path):
        print("File not found.")
        return

    print("\nCalculating hashes...")

    md5 = calculate_hash(file_path, "md5")
    sha1 = calculate_hash(file_path, "sha1")
    sha256 = calculate_hash(file_path, "sha256")

    print("\n========================")
    print("Hash Results")
    print("========================")

    print(f"File:   {file_path}")
    print(f"MD5:    {md5}")
    print(f"SHA1:   {sha1}")
    print(f"SHA256: {sha256}")