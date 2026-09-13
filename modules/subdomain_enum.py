import socket


def subdomain_enumeration():

    domain = input("Enter domain: ")

    domain = domain.replace("https://", "")
    domain = domain.replace("http://", "")
    domain = domain.split("/")[0]

    print("\n========================")
    print("Subdomain Enumeration")
    print("========================")

    try:
        with open("wordlists/subdomains.txt", "r") as file:
            subdomains = file.read().splitlines()
            subdomains = list(dict.fromkeys(subdomains))

    except FileNotFoundError:
        print("Subdomain wordlist not found.")
        return

    found_subdomains = set()

    for subdomain in subdomains:

        hostname = f"{subdomain}.{domain}"

        try:
            ip_address = socket.gethostbyname(hostname)

            print(f"[+] {hostname} -> {ip_address}")

            found_subdomains.add(hostname)

        except socket.gaierror:
            pass

    print(f"\nFound {len(found_subdomains)} subdomain(s).")