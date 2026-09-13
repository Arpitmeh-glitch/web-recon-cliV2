def create_finding(title, severity, description, recommendation):

    finding = {
        "title": title,
        "severity": severity,
        "description": description,
        "recommendation": recommendation
    }

    return finding