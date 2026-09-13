from modules.host_discovery import host_discovery
from modules.port_scanner import port_scanner
from modules.service_detection import service_detection
from modules.banner_grabber import banner_grabber
from modules.os_detection import os_detection
from modules.full_recon import full_recon
from modules.integrity_checker import integrity_checker
import modules.session as session
def recon_menu():

    while True:

        print("\n========================")
        print("Recon")
        print("========================")
        print("1. Host Discovery")
        print("2. Port Scanner")
        print("3. Service Detection")
        print("4. Banner Grab")
        print("5. OS Detection")
        print("6. Full Recon")
        print("7. Back")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            host_discovery()

        elif choice == "2":
            port_scanner()

        elif choice == "3":
            service_detection()

        elif choice == "4":
            banner_grabber()
        elif choice == "5":
            os_detection()

        if choice == "6":
            results = full_recon()

            if results:
                session.last_recon_result = results
        

        elif choice == "7":
            integrity_checker()

        elif choice == "8":
            break

        else:
            print("Invalid choice!")