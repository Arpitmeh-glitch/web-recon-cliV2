from modules.http_analysis import http_analysis
from modules.technology_detection import technology_detection
from modules.dns_intelligence import dns_intelligence
from modules.tls_analysis import tls_analysis
from modules.subdomain_enum import subdomain_enumeration
from modules.whois_intelligence import whois_intelligence
from modules.path_discovery import path_discovery
from modules.ui import error, menu, select_prompt


def web_menu():

    while True:

        menu("Intelligence", [
            (1, "HTTP Analysis"),
            (2, "DNS Intelligence"),
            (3, "TLS Analysis"),
            (4, "Technology Detection"),
            (5, "Subdomain Enumeration"),
            (6, "Web Path Discovery"),
            (7, "WHOIS Intelligence"),
            (8, "Back")
        ])

        choice = select_prompt()

        if choice == "1":
            http_analysis()

        elif choice == "2":
            dns_intelligence()

        elif choice == "3":
            tls_analysis()

        elif choice == "4":
            technology_detection()

        elif choice == "5":
            subdomain_enumeration()

        elif choice == "6":
            path_discovery()

        elif choice == "7":
            whois_intelligence()

        elif choice == "8":
            break

        else:
            error("Invalid choice")