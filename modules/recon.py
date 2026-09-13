from modules.host_discovery import host_discovery
from modules.port_scanner import port_scanner
from modules.service_detection import service_detection
from modules.banner_grabber import banner_grabber
from modules.os_detection import os_detection
from modules.full_recon import full_recon
import modules.session as session
from modules.ui import error, menu, select_prompt


def recon_menu():

    while True:

        menu("Recon", [
            (1, "Host Discovery"),
            (2, "Port Scanner"),
            (3, "Service Detection"),
            (4, "Banner Grab"),
            (5, "OS Detection"),
            (6, "Full Recon"),
            (7, "Back")
        ])

        choice = select_prompt()

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

        elif choice == "6":
            results = full_recon()

            if results:
                session.last_recon_result = results

        elif choice == "7":
            break

        else:
            error("Invalid choice")