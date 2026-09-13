import subprocess
import platform
import re


def get_ttl(target):
    try:
        # Windows and Linux use different ping options
        if platform.system().lower() == "windows":
            command = ["ping", "-n", "1", target]
        else:
            command = ["ping", "-c", "1", target]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=5
        )

        # Search ping output for TTL value
        match = re.search(
            r"ttl[=\s](\d+)",
            result.stdout,
            re.IGNORECASE
        )

        if match:
            return int(match.group(1))

        return None

    except Exception:
        return None


def guess_os(ttl):
    if ttl <= 64:
        return "Linux / Unix-like"

    elif ttl <= 128:
        return "Windows"

    elif ttl <= 255:
        return "Network device / Unix-like"

    return "Unknown"


def os_detection():
    print("\n--- OS Detection ---")

    target = input("Enter target IP or hostname: ").strip()

    print(f"\nAnalyzing {target}...")

    ttl = get_ttl(target)

    if ttl is None:
        print("Could not determine TTL.")
        return

    probable_os = guess_os(ttl)

    print(f"\nTTL: {ttl}")
    print(f"Probable OS: {probable_os}")
    print("Method: TTL Analysis")
    print("Confidence: Low")