from pathlib import Path
from http import HTTPStatus
from urllib.parse import urljoin

import requests


PATH_WORDLIST = Path(__file__).resolve().parent.parent / "wordlists" / "paths.txt"
DISCOVERED_STATUS_CODES = set(range(200, 400)) | {401, 403}


def status_meaning(status_code):
    try:
        return HTTPStatus(status_code).phrase
    except ValueError:
        return "Unknown Status"


def normalize_url(url):
    """Return a URL with a scheme and a single trailing slash."""
    url = url.strip()

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    return url.rstrip("/") + "/"


def load_paths(wordlist_path=PATH_WORDLIST):
    """Load unique, relative paths from a wordlist."""
    with open(wordlist_path, "r", encoding="utf-8") as file:
        paths = []

        for line in file:
            path = line.strip()

            if not path or path.startswith("#"):
                continue

            paths.append(path.lstrip("/"))

    return list(dict.fromkeys(paths))


def discover_paths(base_url, paths=None, request_get=requests.get, show_results=False):
    """Return discovered paths and their HTTP status codes."""
    base_url = normalize_url(base_url)
    paths = load_paths() if paths is None else paths
    discovered = []

    for path in paths:
        target_url = urljoin(base_url, path)

        try:
            response = request_get(
                target_url,
                allow_redirects=False,
                timeout=5,
                headers={"User-Agent": "CyberReconX/1.0"},
            )
        except requests.exceptions.RequestException:
            continue

        if response.status_code in DISCOVERED_STATUS_CODES:
            result = (target_url, response.status_code)
            discovered.append(result)

            if show_results:
                print(
                    f"[+] {target_url} -> {response.status_code} "
                    f"({status_meaning(response.status_code)})"
                )

    return discovered


def path_discovery():
    url = input("Enter website URL: ")

    print("\n========================")
    print("Web Path Discovery")
    print("========================")

    try:
        paths = discover_paths(url, show_results=True)
    except FileNotFoundError:
        print("Path wordlist not found.")
        return

    print(f"\nFound {len(paths)} path(s).")
