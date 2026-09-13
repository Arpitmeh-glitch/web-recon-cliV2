import os
import re


def analyze_log(file_path):
    try:
        with open(file_path, "r", errors="ignore") as file:
            lines = file.readlines()

        errors = 0
        warnings = 0
        failed_logins = 0
        ip_addresses = []

        for line in lines:
            lower_line = line.lower()

            # Count errors
            if "error" in lower_line:
                errors += 1

            # Count warnings
            if "warning" in lower_line or "warn" in lower_line:
                warnings += 1

            # Look for common failed login messages
            if (
                "failed password" in lower_line
                or "authentication failure" in lower_line
                or "login failed" in lower_line
            ):
                failed_logins += 1

            # Extract IPv4 addresses
            ips = re.findall(
                r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
                line
            )

            ip_addresses.extend(ips)

        return {
            "total_lines": len(lines),
            "errors": errors,
            "warnings": warnings,
            "failed_logins": failed_logins,
            "ip_addresses": ip_addresses
        }

    except Exception:
        return None


def log_analyzer():
    print("\n========================")
    print("Log Analyzer")
    print("========================")

    file_path = input("Enter log file path: ").strip()

    if not os.path.isfile(file_path):
        print("File not found.")
        return

    results = analyze_log(file_path)

    if results is None:
        print("Could not analyze log.")
        return

    print("\n========================")
    print("Log Analysis Results")
    print("========================")

    print(f"File:          {os.path.basename(file_path)}")
    print(f"Total Lines:   {results['total_lines']}")
    print(f"Errors:        {results['errors']}")
    print(f"Warnings:      {results['warnings']}")
    print(f"Failed Logins: {results['failed_logins']}")

    unique_ips = sorted(set(results["ip_addresses"]))

    print(f"Unique IPs:    {len(unique_ips)}")

    if unique_ips:
        print("\nIP Addresses:")

        for ip in unique_ips:
            print(f"  {ip}")