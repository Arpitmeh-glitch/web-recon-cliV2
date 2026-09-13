from modules.file_hash import file_hash_analyzer
from modules.file_metadata import file_metadata_analyzer
from modules.file_signature import file_signature_checker
from modules.string_extractor import string_extractor
from modules.log_analyzer import log_analyzer
from modules.integrity_checker import integrity_checker
from modules.metadata_writer import metadata_writer
from modules.ui import error, menu, select_prompt


def dfir_menu():

    while True:

        menu("DFIR", [
            (1, "File Hash Analyzer"),
            (2, "File Metadata Analyzer"),
            (3, "File Signature Checker"),
            (4, "String Extractor"),
            (5, "Log Analyzer"),
            (6, "Directory Integrity Checker"),
            (7, "Metadata Writer"),
            (8, "Back")
        ])

        choice = select_prompt()

        if choice == "1":
            file_hash_analyzer()
        elif choice == "2":
            file_metadata_analyzer()
        elif choice == "3":
            file_signature_checker()
        elif choice == "4":
            string_extractor()
        elif choice == "5":
            log_analyzer()
        elif choice == "6":
            integrity_checker()
        elif choice == "7":
            metadata_writer()

        elif choice == "8":
            break

        else:
            error("Invalid choice")