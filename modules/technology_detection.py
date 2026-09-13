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

        # Server detection
        if server:
            print(f"Server: {server}")
        else:
            print("Server: Not detected")

        # Backend technology detection
        if powered_by:
            print(f"Powered By: {powered_by}")
        else:
            print("Powered By: Not detected")

        # CMS detection
        detected_cms = detect_cms(html)

        if detected_cms:
            print(f"CMS: {detected_cms}")
        else:
            print("CMS: Not detected")

        # Frontend technology detection
        detected_technologies = detect_frontend(html)

        print("\nFrontend Technologies:")

        if detected_technologies:
            for technology in detected_technologies:
                print(f"- {technology}")
        else:
            print("None detected")

    except requests.exceptions.RequestException:
        print("Could not connect to the website.")


def detect_cms(html):

    cms_fingerprints = {
        "WordPress": ["wp-content", "wp-includes"],
        "Drupal": ["sites/default/files", "drupalsettings"],
        "Joomla": ["/media/system/js/", "joomla!"]
    }

    for cms, fingerprints in cms_fingerprints.items():

        for fingerprint in fingerprints:

            if fingerprint in html:
                return cms

    return None


def detect_frontend(html):

    frontend_fingerprints = {
        "Bootstrap": ["bootstrap.min.css", "bootstrap.min.js"],
        "React": ["react.js", "react.min.js", "react-dom"],
        "Vue.js": ["vue.js", "vue.min.js"],
        "jQuery": ["jquery.js", "jquery.min.js"]
    }

    detected_technologies = []

    for technology, fingerprints in frontend_fingerprints.items():

        for fingerprint in fingerprints:

            if fingerprint in html:
                detected_technologies.append(technology)
                break

    return detected_technologies