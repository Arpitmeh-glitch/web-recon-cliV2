import socket
import ssl


def service_detection():

    target = input("Enter hostname or IP: ").strip()

    try:
        port = int(input("Enter port: "))

        if port < 1 or port > 65535:
            print("Port must be between 1 and 65535.")
            return

    except ValueError:
        print("Invalid port.")
        return

    try:
        target_ip = socket.gethostbyname(target)

    except socket.gaierror:
        print("Could not resolve target.")
        return

    print("\n========================")
    print("Service Detection")
    print("========================")

    print(f"Target: {target}")
    print(f"IP: {target_ip}")
    print(f"Port: {port}")

    if not is_port_open(target_ip, port):
        print("\nPort is not open.")
        return

    print("\nPort State: OPEN")

    standard_service = get_standard_service(port)
    print(f"Expected Service: {standard_service}")

    detected_service, banner = detect_service(
        target,
        target_ip,
        port
    )

    print(f"Detected Service: {detected_service}")
    print(f"Banner: {banner}")


def is_port_open(target_ip, port):

    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    sock.settimeout(1)

    try:
        result = sock.connect_ex(
            (target_ip, port)
        )

        return result == 0

    finally:
        sock.close()


def get_standard_service(port):

    try:
        return socket.getservbyport(
            port,
            "tcp"
        )

    except OSError:
        return "unknown"


def detect_service(target, target_ip, port):

    # Services that usually send a banner immediately
    banner = receive_banner(target_ip, port)

    if banner:

        service = identify_banner(banner)

        if service != "Unknown":
            return service, banner

    # Try HTTP
    http_banner = probe_http(
        target,
        target_ip,
        port
    )

    if http_banner:
        return "HTTP", http_banner

    # Try HTTPS/TLS
    tls_result = probe_tls(
        target,
        target_ip,
        port
    )

    if tls_result:
        return "HTTPS/TLS", tls_result

    return "Unknown", "Not detected"


def receive_banner(target_ip, port):

    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    sock.settimeout(1)

    try:
        sock.connect((target_ip, port))

        data = sock.recv(1024)

        if data:
            return clean_text(data)

    except (
        socket.timeout,
        socket.error
    ):
        pass

    finally:
        sock.close()

    return None


def identify_banner(banner):

    banner_lower = banner.lower()

    if "ssh" in banner_lower:
        return "SSH"

    if "ftp" in banner_lower:
        return "FTP"

    if "smtp" in banner_lower:
        return "SMTP"

    if "mysql" in banner_lower:
        return "MySQL"

    if "redis" in banner_lower:
        return "Redis"

    return "Unknown"


def probe_http(target, target_ip, port):

    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    sock.settimeout(1)

    try:
        sock.connect((target_ip, port))

        request = (
            "HEAD / HTTP/1.1\r\n"
            f"Host: {target}\r\n"
            "Connection: close\r\n"
            "\r\n"
        )

        sock.sendall(request.encode())

        data = sock.recv(2048)

        text = clean_text(data)

        if text.startswith("HTTP/"):
            return extract_http_banner(text)

    except (
        socket.timeout,
        socket.error
    ):
        pass

    finally:
        sock.close()

    return None


def probe_tls(target, target_ip, port):

    try:
        context = ssl.create_default_context()

        with socket.create_connection(
            (target_ip, port),
            timeout=2
        ) as sock:

            with context.wrap_socket(
                sock,
                server_hostname=target
            ) as secure_socket:

                version = secure_socket.version()
                cipher = secure_socket.cipher()

                if cipher:
                    return (
                        f"{version} - {cipher[0]}"
                    )

                return version

    except (
        socket.error,
        ssl.SSLError
    ):
        return None


def extract_http_banner(text):

    server = None

    for line in text.splitlines():

        if line.lower().startswith("server:"):
            server = line.strip()
            break

    if server:
        return server

    lines = text.splitlines()

    if lines:
        return lines[0]

    return "HTTP detected"


def clean_text(data):

    text = data.decode(
        "utf-8",
        errors="ignore"
    )

    text = text.strip()

    if not text:
        return ""

    return text.split("\n")[0][:150]