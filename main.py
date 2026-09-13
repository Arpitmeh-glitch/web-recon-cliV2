from modules.web_recon import web_menu
from modules.recon import recon_menu
from modules.reporting import reporting_menu
from modules.dfir import dfir_menu
from modules.ui import banner, error, info, menu, select_prompt


def show_banner():
    banner()


def show_menu():
    menu("Main Menu", [
        (1, "Recon"),
        (2, "Digital Forensics & IR"),
        (3, "Intelligence"),
        (4, "Reporting"),
        (5, "Exit")
    ])


def main():

    while True:

        show_menu()

        choice = select_prompt()

        if choice == '1':
            info("Opening Recon")
            recon_menu()

        elif choice == '2':
            info("Opening Digital Forensics & IR")
            dfir_menu()

        elif choice == '3':
            info("Opening Intelligence")
            web_menu()

        elif choice == '4':
            info("Opening Reporting")
            reporting_menu()

        elif choice == '5':
            print("\nKatergo session ended.")
            break

        else:
            error("Invalid choice")


if __name__ == "__main__":
    show_banner()
    main()