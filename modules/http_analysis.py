import requests


def http_analysis():

    url = input("Enter URL: ")

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    try:
        response = requests.get(url)

        print(f"\nStatus Code: {response.status_code}")

    except requests.exceptions.RequestException:
        print("Could not connect to the website.")
def get_status_code(response):
    return response.status_code