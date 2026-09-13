import requests


def technology_detection():

    url = input("Enter URL: ")

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    try:
        response = requests.get(url)

        print("\n========================")
        print("Technology Detection")
        print("========================")

        server = response.headers.get("Server")
        powered_by = response.headers.get("X-Powered-By")

        html = response.text.lower()

        if server:
            print(f"Server: {server}")
        else:
            print("Server: Not detected")

        if powered_by:
            print(f"Powered By: {powered_by}")
        else:
            print("Powered By: Not detected")

        cms_fingerprints = {
            "WordPress": ["wp-content", "wp-includes"],
            "Drupal": ["sites/default/files", "drupalsettings"],
            "Joomla": ["/media/system/js/", "joomla!"]
        }
        detected_cms = None

        for cms, fingerprints in cms_fingerprints.items():

            for fingerprint in fingerprints:

                if fingerprint in html:
                    detected_cms = cms
                    break

            if detected_cms:
                break
        if detected_cms:
            print(f"CMS: {detected_cms}")
        else:
            print("CMS: Not detected")
    except requests.exceptions.RequestException:
        print("Could not connect to the website.")