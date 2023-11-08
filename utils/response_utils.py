import requests
import tempfile
import webbrowser
import urllib.parse
from bs4 import BeautifulSoup


def format_response(res: requests.Response):
    formatted = "\n"
    for k, v in res.headers.items():
        formatted += f"{k}: {v}\n"
    formatted += f"\n{res.content.decode('utf-8')}\n\n"
    return formatted


def view_response(index: int, responses: list[requests.Response]):
    print(format_response(responses[index]))


def save_response(index: int, responses: list[requests.Response]):
    filename = input("Enter filename: ")
    with open(filename, "w") as f:
        f.write(format_response(responses[index]))


def view_in_browser(index: int, base_url: str, responses: list[requests.Response]):
    html = responses[index].content.decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    for element in soup.find_all(["a", "link", "script", "img"]):
        for attr in ["href", "src"]:
            if element.get(attr) is not None:
                element[attr] = urllib.parse.urljoin(base_url, element[attr])

    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".html") as f:
        url = "file://" + f.name
        f.write(str(soup))
    webbrowser.open(url)
