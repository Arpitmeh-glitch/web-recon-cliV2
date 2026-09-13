import socket
import dns.resolver
import dns.exception


def dns_intelligence():

    domain = input("Enter domain: ")

    domain = domain.replace("https://", "")
    domain = domain.replace("http://", "")
    domain = domain.split("/")[0]

    try:
        ip_addresses = socket.gethostbyname_ex(domain)[2]

        print("\n========================")
        print("DNS Intelligence")
        print("========================")

        print(f"Domain: {domain}")

        print("\nIPv4 Addresses:")

        for ip in ip_addresses:
            print(f"- {ip}")

            try:
                hostname = socket.gethostbyaddr(ip)[0]
                print(f"  Reverse DNS: {hostname}")

            except socket.herror:
                print("  Reverse DNS: Not found")

        get_dns_records(domain)
        check_email_security(domain)

    except socket.gaierror:
        print("Could not resolve the domain.")


def get_dns_records(domain):

    record_types = [
        "A",
        "AAAA",
        "CNAME",
        "MX",
        "NS",
        "TXT"
    ]

    print("\nDNS Records:")

    for record_type in record_types:

        print(f"\n{record_type} Records:")

        try:
            answers = dns.resolver.resolve(domain, record_type)

            for answer in answers:
                print(f"- {answer}")

        except dns.resolver.NoAnswer:
            print("- None found")

        except dns.resolver.NXDOMAIN:
            print("- Domain does not exist")

        except dns.exception.DNSException:
            print("- Could not retrieve records")
def check_email_security(domain):

    print("\nEmail Security:")

    # SPF Check
    try:
        answers = dns.resolver.resolve(domain, "TXT")

        spf_found = False

        for answer in answers:
            text = answer.to_text()

            if "v=spf1" in text.lower():
                print(f"SPF: Present ({text})")
                spf_found = True
                break

        if not spf_found:
            print("SPF: Not found")

    except dns.exception.DNSException:
        print("SPF: Could not check")

    # DMARC Check
    try:
        dmarc_domain = "_dmarc." + domain

        answers = dns.resolver.resolve(dmarc_domain, "TXT")

        dmarc_found = False

        for answer in answers:
            text = answer.to_text()

            if "v=dmarc1" in text.lower():
                print(f"DMARC: Present ({text})")
                dmarc_found = True
                break

        if not dmarc_found:
            print("DMARC: Not found")

    except dns.exception.DNSException:
        print("DMARC: Not found")