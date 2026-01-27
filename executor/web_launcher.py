import webbrowser

def open_website(url: str):
    if not url.startswith("http"):
        url = "https://" + url
    webbrowser.open(url)
