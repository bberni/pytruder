import re
import ast
import requests
import sys
SPECIAL_SYMBOL = "$"


def modify_request(raw_request, payload):
    # "tnie" zaypytanie na trzy części i zamienia środkową na wyraz ze słownika
    if SPECIAL_SYMBOL in raw_request:
        raw_request = raw_request.split(SPECIAL_SYMBOL)
        raw_request[1] = requests.utils.quote(payload)

    return "".join(raw_request)


def parse_request(request):
    # zamienia zapytanie HTTP w formie tekstowej na słownik,
    # którego może użyć biblioteka requests
    method = re.findall(r"[A-Z]*\S", request)[0]
    request = re.sub(r"[A-Z]*\S", "", request, 1)
    url = re.findall(r"\/\S*", request)[0]
    request = re.sub(r"\/\S*", "", request, 1)
    header_dump = re.findall(r".*:.*[^\n]", request)
    request = re.sub(r".*:.*[^\n]", "", request)
    headers = []
    for header in header_dump:
        header = list(header)
        header.insert(0, '"')
        header.append('"')
        header.insert(header.index(":"), '"')
        header.insert(header.index(":") + 2, '"')
        headers.append("".join(header))
    headers = ast.literal_eval("{" + ",".join(headers) + "}")
    request = re.sub(r"HTTP\S*", "", request)
    request = re.sub("\n", "", request)
    body = request.strip()
    return method, url, headers, body


def send_request(
    method: str, url: str, data: str, headers: dict = {}, timeout: int = 10
):
    response = requests.request(
        method=method, url=url, headers=headers, data=data, timeout=timeout
    )

    return response


def guess_protocol(args):
    #zgaduje protokół -> HTTP albo HTTPS
    method, url, headers, body = args
    try:
        send_request(
            method=method,
            url="https://" + headers["Host"] + url,
            data=body,
            headers=headers,
        )
        return "https"
    except requests.exceptions.SSLError:
        return "http"
