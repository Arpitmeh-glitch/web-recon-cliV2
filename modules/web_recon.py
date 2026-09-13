from modules.http_analysis import http_analysis
from modules.technology_detection import technology_detection
from modules.dns_intelligence import dns_intelligence


def web_menu():

    while True:

        print("\n========================")
        print("Web Intelligence")
        print("========================")
        print("1. HTTP Analysis")
        print("2. DNS Intelligence")
        print("3. TLS Analysis")
        print("4. Technology Detection")
        print("5. Subdomain Enumeration")
        print("6. Back")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            http_analysis()

        elif choice == "2":
            dns_intelligence()

        elif choice == "3":
            print("TLS Analysis")

        elif choice == "4":
            technology_detection()

        elif choice == "5":
            print("Subdomain Enumeration")

        elif choice == "6":
            break

        else:
            print("Invalid choice!")