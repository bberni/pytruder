#!/usr/bin/python3
import re 
import argparse
import requests

SPECIAL_SYMBOL = '$'
def send_request(method: str, url: str, data: str, headers: dict = {}, timeout: int = 10):
  
    response = requests.request(method=method, url=url, headers=headers, data=data, timeout=timeout)
    
    return response





#print(send_request('GET', 'https://webhook.site/9cab2bb2-b0f3-423f-acf1-b1756efc3dad', data="test=test1"))

def main(): 
    parser = argparse.ArgumentParser()
    parser.add_argument('request', type=str, help=f'add a request file with {SPECIAL_SYMBOL} markings')
    parser.add_argument('payload', type=str, help='add payload file with inputs separated by newlines')
    print(send_request('GET', 'https://webhook.site/9cab2bb2-b0f3-423f-acf1-b1756efc3dad', data="test=test1"))



if __name__ == "__main__": 
    main()

