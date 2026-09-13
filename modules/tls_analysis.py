import socket
import ssl


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
                print(f"TLS Version: {secure_socket.version()}")

    except (socket.error, ssl.SSLError):
        print("Could not establish a TLS connection.")
        