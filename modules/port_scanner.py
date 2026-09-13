import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


# Common ports used by Quick Scan
QUICK_PORTS = [
    21, 22, 23, 25, 53,
    80, 110, 111, 135, 139,
    143, 389, 443, 445, 465,
    587, 636, 993, 995, 1433,
    1521, 2049, 3306, 3389, 5432,
    5900, 6379, 8080, 8443, 27017
]


def port_scanner():

    target = input("Enter hostname or IP: ").strip()

    try:
        target_ip = socket.gethostbyname(target)

    except socket.gaierror:
        print("Could not resolve target.")
        return

    print("\n================================")
    print("Port Scanner")
    print("================================")
    print(f"Target: {target}")
    print(f"IP:     {target_ip}")

    print("\nScan Type:")
    print("1. Quick Scan")
    print("2. Ports 1-1024")
    print("3. Custom Range")
    print("4. Full Scan (1-65535)")

    choice = input("\nEnter your choice: ")

    ports = get_ports(choice)

    if not ports:
        return

    workers = get_scan_speed()

    print("\n================================")
    print("Scanning")
    print("================================")
    print(f"Ports:   {len(ports)}")
    print(f"Workers: {workers}")
    print()

    start_time = time.time()

    open_ports = scan_ports(
        target_ip,
        ports,
        workers
    )

    scan_time = time.time() - start_time

    print_results(
        target,
        target_ip,
        open_ports,
        scan_time,
        len(ports)
    )


def get_ports(choice):

    if choice == "1":
        return QUICK_PORTS

    elif choice == "2":
        return list(range(1, 1025))

    elif choice == "3":

        try:
            start_port = int(input("Start port: "))
            end_port = int(input("End port: "))

        except ValueError:
            print("Invalid port number.")
            return []

        if start_port < 1 or end_port > 65535:
            print("Ports must be between 1 and 65535.")
            return []

        if start_port > end_port:
            print("Start port cannot be greater than end port.")
            return []

        return list(range(start_port, end_port + 1))

    elif choice == "4":
        return list(range(1, 65536))

    else:
        print("Invalid choice.")
        return []


def get_scan_speed():

    print("\nScan Speed:")
    print("1. Slow")
    print("2. Normal")
    print("3. Fast")

    choice = input("\nEnter your choice: ")

    if choice == "1":
        return 25

    elif choice == "3":
        return 200

    return 100


def scan_ports(target_ip, ports, workers):

    open_ports = []

    with ThreadPoolExecutor(max_workers=workers) as executor:

        futures = {}

        for port in ports:

            future = executor.submit(
                check_port,
                target_ip,
                port
            )

            futures[future] = port

        for future in as_completed(futures):

            port = futures[future]

            try:
                is_open = future.result()

            except Exception:
                continue

            if is_open:

                service = get_service_name(port)
                banner = grab_banner(target_ip, port)

                result = {
                    "port": port,
                    "service": service,
                    "banner": banner
                }

                open_ports.append(result)

                print(
                    f"[+] {port}/tcp OPEN  "
                    f"{service}"
                )

    open_ports.sort(
        key=lambda result: result["port"]
    )

    return open_ports


def check_port(target_ip, port):

    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    sock.settimeout(0.5)

    try:
        result = sock.connect_ex(
            (target_ip, port)
        )

        return result == 0

    except socket.error:
        return False

    finally:
        sock.close()


def get_service_name(port):

    try:
        return socket.getservbyport(
            port,
            "tcp"
        )

    except OSError:
        return "unknown"


def grab_banner(target_ip, port):

    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    sock.settimeout(1)

    try:
        sock.connect((target_ip, port))

        # Some services send a banner immediately.
        try:
            banner = sock.recv(1024)

            if banner:
                return clean_banner(banner)

        except socket.timeout:
            pass

        # HTTP servers usually wait for a request.
        if port in [80, 8080, 8000, 8888]:

            request = (
                "HEAD / HTTP/1.1\r\n"
                f"Host: {target_ip}\r\n"
                "Connection: close\r\n\r\n"
            )

            sock.sendall(request.encode())

            banner = sock.recv(1024)

            if banner:
                return extract_http_server(banner)

    except (
        socket.timeout,
        socket.error,
        ConnectionError
    ):
        pass

    finally:
        sock.close()

    return "Not detected"


def clean_banner(banner):

    try:
        text = banner.decode(
            "utf-8",
            errors="ignore"
        )

        text = text.strip()

        if not text:
            return "Not detected"

        # Keep CLI output on one line.
        return text.split("\n")[0][:100]

    except Exception:
        return "Not detected"


def extract_http_server(banner):

    try:
        text = banner.decode(
            "utf-8",
            errors="ignore"
        )

        for line in text.splitlines():

            if line.lower().startswith("server:"):
                return line.strip()

        first_line = text.splitlines()

        if first_line:
            return first_line[0][:100]

    except Exception:
        pass

    return "Not detected"


def print_results(
    target,
    target_ip,
    open_ports,
    scan_time,
    ports_scanned
):

    print("\n================================")
    print("Scan Results")
    print("================================")

    print(f"Target:        {target}")
    print(f"IP:            {target_ip}")
    print(f"Ports scanned: {ports_scanned}")
    print(f"Open ports:    {len(open_ports)}")
    print(f"Scan time:     {scan_time:.2f} seconds")

    if not open_ports:
        print("\nNo open ports detected.")
        return

    print("\nPORT\tSTATE\tSERVICE\tBANNER")

    for result in open_ports:

        port = result["port"]
        service = result["service"]
        banner = result["banner"]

        print(
            f"{port}/tcp\t"
            f"OPEN\t"
            f"{service}\t"
            f"{banner}"
        )