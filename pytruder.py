#!/usr/bin/python3
import argparse
import re
import concurrent.futures
from utils.request_utils import *
from utils.table_utils import *
from utils.response_utils import *
import time


def run(args: tuple):
    #funkcja bezpośrednio odpowiedzialna za wysyłanie zapytania HTTP i przetwarzanie odpowiedzi
    global protocol
    global request
    index = args[0]
    p = args[1]
    method, url, headers, body = parse_request(modify_request(request, p))
    response = send_request(
        method=method,
        url=protocol + "://" + headers["Host"] + url,
        data=body,
        headers=headers,
    )
    response_number = str(index)
    payload_text = p
    status_code = str(response.status_code)
    response_time = str(round(response.elapsed.total_seconds() * 1000))
    response_length = str(len(response.content))
    return [
        (
            response_number,
            payload_text,
            status_code,
            response_time,
            response_length,
            index,
        ),
        response,
    ]


def main():
    global protocol
    global request
    t1 = time.perf_counter()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "request", type=str, help=f"add a request file with {SPECIAL_SYMBOL} markings"
    )
    parser.add_argument(
        "payload", type=str, help="add payload file with inputs separated by newlines"
    )
    args = parser.parse_args() #przetwarzanie argumentów z CLI

    request_file = args.request
    payload_file = args.payload

    with open(request_file, "r") as f: # wczytywanie pliku z zapytaniem HTTP
        request = f.read()
        host = re.findall(r"Host: \S*", request)[0][6:]
        print(host)
    with open(payload_file, "r") as f: # wczytywanie pliku ze słownikiem
        payloads = f.read().split("\n")

    print_border()
    print(create_row("Request", "Payload", "Status Code", "Response Time", "Length", 0))
    print_border()

    responses = []    
    protocol = guess_protocol(parse_request(modify_request(request, payloads[0]))) 
    with concurrent.futures.ThreadPoolExecutor() as executor:
        #żeby znacząco przyspieszyć wysyłanie zapytań stosujemy multithreading
        for result in executor.map(run, enumerate(payloads)):
            print(create_row(*result[0]))
            responses.append(result[1])

    print_border()
    print(time.perf_counter() - t1)
    while True: # główna pętla programu
        choice = input(
            "Enter 1 to view a response, 2 to save a response, 3 to view response in browser, or 4 to exit and press ENTER: "
        )
        match choice:
            case "1":
                r = input("Enter response number: ")
                view_response(int(r), responses)
            case "2":
                r = input("Enter response number: ")
                save_response(int(r), responses)
            case "3":
                r = input("Enter response number: ")
                view_in_browser(int(r), protocol + "://" + host, responses)
            case "4":
                exit()
            case _:
                print("Invalid choice")


if __name__ == "__main__":
    main()
