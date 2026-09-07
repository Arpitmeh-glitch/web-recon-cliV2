import requests


def http_analysis():

    url = input("Enter URL: ")

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    try:
        response = requests.get(url)

        print(f"\nStatus Code: {response.status_code}")

        server = response.headers.get("Server")
        print(f"Server: {server}")

        content_type = response.headers.get("Content-Type")
        print(f"Content-Type: {content_type}")

        content_length = response.headers.get("Content-Length")
        print(f"Content-Length: {content_length}")

        findings = []

        security_headers = {
            "Strict-Transport-Security": "Medium",
            "Content-Security-Policy": "Medium",
            "X-Frame-Options": "Low",
            "X-Content-Type-Options": "Low"
        }

        print("\nSecurity Headers:")

        for header, severity in security_headers.items():
            value = response.headers.get(header)

            if value:
                print(f"{header}: Present")
            else:
                print(f"{header}: Missing")
                findings.append({
            "title": f"Missing {header}",
            "severity": severity
        })

        print("\nFindings:")

        if findings:
            for finding in findings:
                print(f"[{finding['severity']}] {finding['title']}")
        else:
            print("No security header issues detected.")

    except requests.exceptions.RequestException:
        print("Could not connect to the website.")


def get_status_code(response):
    return response.status_code