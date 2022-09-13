#!/usr/bin/python3
import re 
import os
import ast
import argparse
import requests
import colorama

os.chdir('/home/bberni/pytruder')
SPECIAL_SYMBOL = '$'

def modify_request(raw_request, payload): 
    if SPECIAL_SYMBOL in raw_request:
        raw_request = raw_request.split(SPECIAL_SYMBOL)
        raw_request[1] = requests.utils.quote(payload) #exprimental 
    
    return ''.join(raw_request)
    

def parse_request(request):
    method = re.findall(r'[A-Z]*\S', request)[0]
    request = re.sub(r'[A-Z]*\S', '', request, 1) 
    url = re.findall(r'\/\S*', request)[0]
    request = re.sub(r'\/\S*','', request, 1)
    header_dump = re.findall(r'.*:.*[^\n]', request)
    request = re.sub(r'.*:.*[^\n]', '', request)
    headers = []
    for header in header_dump: 
        header = list(header)
        header.insert(0, '"')
        header.append('"')
        header.insert(header.index(':'), '"')
        header.insert(header.index(':') + 2, '"')
        headers.append(''.join(header))
    headers = ast.literal_eval('{' + ','.join(headers) + '}')
    request = re.sub(r'HTTP\S*', '', request)
    request = re.sub('\n', '', request)
    body = request.strip()

    return method, url, headers, body

def send_request(method: str, url: str, data: str, headers: dict = {}, timeout: int = 10):
    response = requests.request(method=method, url=url, headers=headers, data=data, timeout=timeout)
    
    return response

def create_row(number, payload, code, time, length, index):
    if index % 2 == 0: 
        row = f'|{number.rjust(20)} |{payload.rjust(20)} |{code.rjust(20)} |{time.rjust(20)} |{length.rjust(20)} |'
    else: 
        row = '|' + f'{number.rjust(20)} |{payload.rjust(20)} |{code.rjust(20)} |{time.rjust(20)} |{length.rjust(20)} ' + colorama.Style.RESET_ALL + '|' #+ colorama.Fore.BLACK + colorama.Back.WHITE
    return row
#print(send_request('GET', 'https://webhook.site/9cab2bb2-b0f3-423f-acf1-b1756efc3dad', data="test=test1"))
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

    print(f'+{"-" * 109}+')
    print(create_row('Request', 'Payload', 'Status Code', 'Response Time', 'Length', 0))
    print(f'+{"-" * 109}+')
    for index, p in enumerate(payloads):
        method, url, headers, body = parse_request(modify_request(request, p)) #modify_request(request, p)
        response = send_request(method=method, url='https://' + headers['Host'] + url, data=body, headers=headers)
        response_number = str(index)
        payload_text = p
        status_code = str(response.status_code)
        response_time = str(round(response.elapsed.total_seconds() * 1000))
        response_length = str(len(response.content))
        #print(f'|{"-" * 109}|')
        print(create_row(response_number, payload_text, status_code, response_time, response_length, index))
        
    print(f'+{"-" * 109}+')

if __name__ == "__main__": 
    main()

