import socket


def grab_banner(target, port):
    try:
        # Create a TCP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Don't wait forever
        sock.settimeout(3)

        # Connect to the target
        sock.connect((target, port))

        # Some services send a banner immediately
        try:
            banner = sock.recv(1024)

            if banner:
                sock.close()
                return banner.decode(errors="ignore").strip()

        except socket.timeout:
            pass

        # Some services like HTTP need us to send something first
        if port in [80, 8080, 8000]:
            request = (
                f"HEAD / HTTP/1.1\r\n"
                f"Host: {target}\r\n"
                f"Connection: close\r\n\r\n"
            )

            sock.send(request.encode())

            banner = sock.recv(1024)

            sock.close()

            return banner.decode(errors="ignore").strip()

        sock.close()
        return None

    except Exception:
        return None


def banner_grabber():
    print("\n--- Banner Grabber ---")

    target = input("Enter target IP or hostname: ").strip()

    try:
        port = int(input("Enter port: "))
    except ValueError:
        print("Invalid port.")
        return

    if port < 1 or port > 65535:
        print("Port must be between 1 and 65535.")
        return

    print(f"\nConnecting to {target}:{port}...")

    banner = grab_banner(target, port)

    if banner:
        print("\nBanner found:")
        print("-" * 40)
        print(banner)
        print("-" * 40)

    else:
        print("\nNo banner received.")