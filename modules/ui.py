import os


NO_COLOR = os.environ.get("NO_COLOR") == "1"

if NO_COLOR:
    CYAN = ""
    GREEN = ""
    YELLOW = ""
    RED = ""
    BLUE = ""
    BOLD = ""
    RESET = ""
else:
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    BLUE = "\033[34m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


def banner():
    print(f"{CYAN}{BOLD}")
    print("  KATERGO")
    print("  K   K  AAAAA  TTTTT  EEEEE  RRRR   GGGG   OOO")
    print("  K  K   A   A    T    E      R   R  G      O   O")
    print("  KKK    AAAAA    T    EEEE   RRRR   G  GG  O   O")
    print("  K  K   A   A    T    E      R R    G   G  O   O")
    print("  K   K  A   A    T    EEEEE  R  RR  GGGG    OOO")
    print(f"{RESET}")
    print(f"{CYAN}Recon | DFIR | Intelligence | Reporting{RESET}")


def section_header(title):
    line = "=" * (len(title) + 8)
    print(f"\n{CYAN}{line}")
    print(f"  {title.upper()}")
    print(f"{line}{RESET}")


def menu(title, options):
    width = max(len(title) + 4, max(len(f"[{number}] {label}") for number, label in options) + 4)
    border = "=" * width

    print(f"\n{CYAN}{border}")
    print(f"  {title.upper()}")
    print(border)

    for number, label in options:
        print(f"  [{number}] {label}")

    print(f"{border}{RESET}")


def success(message):
    print(f"{GREEN}[+] {message}{RESET}")


def warning(message):
    print(f"{YELLOW}[!] {message}{RESET}")


def error(message):
    print(f"{RED}[-] {message}{RESET}")


def info(message):
    print(f"{BLUE}[*] {message}{RESET}")


def select_prompt():
    return input("Select > ")
