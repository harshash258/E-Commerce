def convert(url):
    url = url.replace(" ", "_")
    url = url.replace("(", "_")
    url = url.replace(")", "_")
    url = url.lower()
    return url
