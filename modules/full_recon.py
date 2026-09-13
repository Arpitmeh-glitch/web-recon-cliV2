import socket
import time

from modules.banner_grabber import grab_banner
from modules.os_detection import get_ttl, guess_os


# Common ports for the first version of Full Recon
COMMON_PORTS = [
    21, 22, 23, 25, 53, 80, 110, 139,
    143, 443, 445, 3306, 3389, 5432,
    5900, 8000, 8080, 8443
]


def check_port(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)

        result = sock.connect_ex((target, port))
        sock.close()

        return result == 0

    except:
        return False


def get_service(port):
    try:
        return socket.getservbyport(port)
    except:
        return "Unknown"


def full_recon():
    print("\n==============================")
    print("Katergo - Full Recon Scan")
    print("==============================")

    target = input("Enter hostname or IP: ").strip()

    try:
        ip = socket.gethostbyname(target)
    except socket.gaierror:
        print("Could not resolve target.")
        return

    print(f"\nTarget: {target}")
    print(f"IP:     {ip}")

    start_time = time.time()

    # -------------------------
    # OS Detection
    # -------------------------

    print("\n[+] Detecting probable OS...")

    ttl = get_ttl(target)

    if ttl:
        probable_os = guess_os(ttl)
        print(f"TTL: {ttl}")
        print(f"Probable OS: {probable_os}")
    else:
        print("OS could not be estimated.")

    # -------------------------
    # Port Scanning
    # -------------------------

    print("\n[+] Scanning common ports...")

    open_ports = []

    for port in COMMON_PORTS:
        if check_port(ip, port):
            open_ports.append(port)

    # -------------------------
    # Results
    # -------------------------

    print("\n==============================")
    print("Recon Results")
    print("==============================")

    if not open_ports:
        print("\nNo open common ports detected.")

    else:
        print("\nPORT\tSERVICE\tBANNER")
        print("-" * 60)

        for port in open_ports:
            service = get_service(port)

            banner = grab_banner(ip, port)

            if not banner:
                banner = "Not detected"

            # Don't dump huge banners into the terminal
            banner = banner.replace("\n", " ")

            if len(banner) > 50:
                banner = banner[:50] + "..."

            print(f"{port}\t{service}\t{banner}")

    end_time = time.time()

    print("\n------------------------------")
    print(f"Open ports: {len(open_ports)}")
    print(f"Scan time: {end_time - start_time:.2f} seconds")
    print("------------------------------")
    results = {
        "target": target,
        "ip": ip,
        "os": probable_os if ttl else "Unknown",
        "open_ports": open_ports,
        "scan_time": end_time - start_time
    }

    return results