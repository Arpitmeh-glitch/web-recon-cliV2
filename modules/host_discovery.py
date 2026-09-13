import subprocess
import ipaddress


def host_discovery():

    print("\n========================")
    print("Host Discovery")
    print("========================")
    print("1. Single Host")
    print("2. Subnet")

    choice = input("\nEnter your choice: ")

    if choice == "1":
        target = input("Enter hostname or IP: ").strip()
        check_host(target)

    elif choice == "2":
        subnet = input("Enter subnet (example: 192.168.1.0/24): ").strip()
        scan_subnet(subnet)

    else:
        print("Invalid choice.")


def check_host(target):

    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "1", target],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        if result.returncode == 0:
            print(f"[+] {target} is reachable")
            return True

        return False

    except FileNotFoundError:
        print("Ping command was not found.")
        return False


def scan_subnet(subnet):

    try:
        network = ipaddress.ip_network(subnet, strict=False)

    except ValueError:
        print("Invalid subnet.")
        return

    # Keep this beginner version to small networks.
    if network.num_addresses > 256:
        print("Subnet is too large. Use /24 or smaller.")
        return

    print(f"\nScanning {network}...\n")

    live_hosts = []

    for ip in network.hosts():

        ip = str(ip)

        if check_host(ip):
            live_hosts.append(ip)

    print("\n========================")
    print("Discovery Complete")
    print("========================")
    print(f"Live hosts found: {len(live_hosts)}")