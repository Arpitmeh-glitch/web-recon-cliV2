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

        hsts = response.headers.get("Strict-Transport-Security")

        if hsts:
            print(f"HSTS: Present ({hsts})")
        else:
            print("HSTS: Missing")

    except requests.exceptions.RequestException:
        print("Could not connect to the website.")


def get_status_code(response):
    return response.status_code