import socket
import ssl
from datetime import datetime, timezone
from utils.findings import create_finding


def tls_analysis():

    domain = input("Enter domain: ")

    domain = domain.replace("https://", "")
    domain = domain.replace("http://", "")
    domain = domain.split("/")[0]

    try:
        context = ssl.create_default_context()

        with socket.create_connection((domain, 443)) as sock:

            with context.wrap_socket(
                sock,
                server_hostname=domain
            ) as secure_socket:

                certificate = secure_socket.getpeercert()

                print("\n========================")
                print("TLS Analysis")
                print("========================")

                print(f"Domain: {domain}")

                # TLS version
                tls_version = secure_socket.version()
                print(f"TLS Version: {tls_version}")

                # Cipher information
                cipher = secure_socket.cipher()

                if cipher:
                    print(f"Cipher: {cipher[0]}")
                    print(f"Encryption Bits: {cipher[2]}")
                else:
                    print("Cipher: Not detected")

                # Certificate information
                subject = get_certificate_name(
                    certificate.get("subject", [])
                )

                issuer = get_certificate_name(
                    certificate.get("issuer", [])
                )

                expiry_date = certificate.get("notAfter")

                print(f"Subject: {subject}")
                print(f"Issuer: {issuer}")
                print(f"Expires: {expiry_date}")

                # Certificate expiry check
                if expiry_date:

                    expiry = datetime.strptime(
                        expiry_date,
                        "%b %d %H:%M:%S %Y %Z"
                    )

                    expiry = expiry.replace(tzinfo=timezone.utc)

                    current_time = datetime.now(timezone.utc)

                    days_left = (expiry - current_time).days

                    print(f"Days Until Expiry: {days_left}")

                    check_certificate_expiry(days_left)

                # TLS version check
                check_tls_version(tls_version)

    except (socket.error, ssl.SSLError):
        print("Could not establish a TLS connection.")


def get_certificate_name(data):

    for item in data:

        for key, value in item:

            if key == "commonName":
                return value

    return "Not found"


def check_certificate_expiry(days_left):

    if days_left < 0:

        finding = create_finding(
            "Certificate Expired",
            "High",
            f"The TLS certificate expired {-days_left} days ago.",
            "Replace the expired TLS certificate immediately."
        )

        print_finding(finding)

    elif days_left < 30:

        finding = create_finding(
            "Certificate Expiring Soon",
            "Medium",
            f"The TLS certificate expires in {days_left} days.",
            "Renew the TLS certificate before it expires."
        )

        print_finding(finding)


def check_tls_version(tls_version):

    if tls_version in ["TLSv1", "TLSv1.1"]:

        finding = create_finding(
            "Outdated TLS Version",
            "High",
            f"The server is using {tls_version}.",
            "Disable old TLS versions and use TLS 1.2 or TLS 1.3."
        )

        print_finding(finding)


def print_finding(finding):

    print("\nFinding:")
    print(f"[{finding['severity']}] {finding['title']}")
    print(f"Description: {finding['description']}")
    print(f"Recommendation: {finding['recommendation']}")