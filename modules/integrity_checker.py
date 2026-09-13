import os
import hashlib
import json


def calculate_hash(file_path):
    try:
        hash_object = hashlib.sha256()

        with open(file_path, "rb") as file:
            while True:
                chunk = file.read(4096)

                if not chunk:
                    break

                hash_object.update(chunk)

        return hash_object.hexdigest()

    except Exception:
        return None


def scan_directory(directory):
    files = {}

    for root, folders, filenames in os.walk(directory):

        for filename in filenames:
            file_path = os.path.join(root, filename)

            file_hash = calculate_hash(file_path)

            if file_hash:
                relative_path = os.path.relpath(file_path, directory)
                files[relative_path] = file_hash

    return files


def create_baseline(directory, baseline_file):
    files = scan_directory(directory)

    try:
        with open(baseline_file, "w") as file:
            json.dump(files, file, indent=4)

        print(f"\nBaseline created successfully.")
        print(f"Files recorded: {len(files)}")

    except Exception as error:
        print(f"Could not create baseline: {error}")


def check_integrity(directory, baseline_file):

    if not os.path.isfile(baseline_file):
        print("Baseline file not found.")
        return

    try:
        with open(baseline_file, "r") as file:
            old_files = json.load(file)

    except Exception:
        print("Could not read baseline.")
        return

    current_files = scan_directory(directory)

    new_files = []
    modified_files = []
    deleted_files = []

    # Check current files
    for file_path, file_hash in current_files.items():

        if file_path not in old_files:
            new_files.append(file_path)

        elif file_hash != old_files[file_path]:
            modified_files.append(file_path)

    # Check for deleted files
    for file_path in old_files:

        if file_path not in current_files:
            deleted_files.append(file_path)

    print("\n========================")
    print("Integrity Results")
    print("========================")

    print(f"New Files:      {len(new_files)}")
    print(f"Modified Files: {len(modified_files)}")
    print(f"Deleted Files:  {len(deleted_files)}")

    if new_files:
        print("\n[+] New Files:")
        for file_path in new_files:
            print(f"  {file_path}")

    if modified_files:
        print("\n[!] Modified Files:")
        for file_path in modified_files:
            print(f"  {file_path}")

    if deleted_files:
        print("\n[-] Deleted Files:")
        for file_path in deleted_files:
            print(f"  {file_path}")

    if not new_files and not modified_files and not deleted_files:
        print("\nNo changes detected.")


def integrity_checker():

    print("\n========================")
    print("Directory Integrity Checker")
    print("========================")

    directory = input("Enter directory path: ").strip()

    if not os.path.isdir(directory):
        print("Directory not found.")
        return

    print("\n1. Create Baseline")
    print("2. Check Integrity")

    choice = input("\nEnter your choice: ").strip()

    baseline_file = "baseline.json"

    if choice == "1":
        create_baseline(directory, baseline_file)

    elif choice == "2":
        check_integrity(directory, baseline_file)

    else:
        print("Invalid choice.")