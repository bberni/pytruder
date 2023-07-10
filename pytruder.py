#!/usr/bin/python3
import argparse
import sys
import pynput
from utils.request_utils import * 
from utils.table_utils import *
from utils.response_utils import * 


def main(): 
    parser = argparse.ArgumentParser()
    parser.add_argument('request', type=str, help=f'add a request file with {SPECIAL_SYMBOL} markings')
    parser.add_argument('payload', type=str, help='add payload file with inputs separated by newlines')
    args = parser.parse_args()
   
    request_file = args.request
    payload_file = args.payload 
    
    with open(request_file, 'r') as f: 
        request = f.read()
    with open(payload_file, 'r') as f: 
        payloads = f.read().split('\n')

    print_border()
    print(create_row('Request', 'Payload', 'Status Code', 'Response Time', 'Length', 0))
    print_border()

    responses = []
    protocol = guess_protocol(parse_request(modify_request(request, payloads[0])))
    for index, p in enumerate(payloads):
        method, url, headers, body = parse_request(modify_request(request, p)) 
        response = send_request(method=method, url=protocol + '://' + headers['Host'] + url, data=body, headers=headers)
        response_number = str(index)
        payload_text = p
        status_code = str(response.status_code)
        response_time = str(round(response.elapsed.total_seconds() * 1000))
        response_length = str(len(response.content)) 
        responses.append(response)
        print(create_row(response_number, payload_text, status_code, response_time, response_length, index))
    print_border()
    while True: 
        choice = input("Enter 1 to view a response, 2 to save a response, or 3 to exit and press ENTER: ")
        match choice: 
            case "1": 
                r = input("Enter response number: ") 
                view_response(int(r), responses)
            case "2":
                r = input("Enter response number: ")  
                save_response(int(r), responses)
            case "3":
                exit()
            case _: 
                print("Invalid choice")

if __name__ == "__main__": 
    main()


