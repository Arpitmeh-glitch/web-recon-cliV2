import whois


def whois_lookup(domain):
    try:
        information = whois.whois(domain)

        return {
            "domain_name": information.domain_name,
            "registrar": information.registrar,
            "creation_date": information.creation_date,
            "expiration_date": information.expiration_date,
            "name_servers": information.name_servers
        }

    except Exception:
        return None


def whois_intelligence():
    print("\n========================")
    print("WHOIS Intelligence")
    print("========================")

    domain = input("Enter domain: ").strip()

    # Remove URL parts if user enters a full URL
    domain = domain.replace("https://", "")
    domain = domain.replace("http://", "")
    domain = domain.split("/")[0]

    print(f"\nLooking up {domain}...")

    results = whois_lookup(domain)

    if results is None:
        print("WHOIS lookup failed.")
        return

    print("\n========================")
    print("WHOIS Results")
    print("========================")

    print(f"Domain:          {results['domain_name']}")
    print(f"Registrar:       {results['registrar']}")
    print(f"Creation Date:   {results['creation_date']}")
    print(f"Expiration Date: {results['expiration_date']}")

    print("\nName Servers:")

    if results["name_servers"]:
        for server in results["name_servers"]:
            print(f"  {server}")

    else:
        print("  Not found")