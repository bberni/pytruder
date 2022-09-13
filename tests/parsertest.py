import os
import re
import ast
os.chdir('/home/bberni/pytruder/')

with open('test.txt' , 'r') as f: 
    dump = f.read()

a = re.findall(r'.*:.*[^\n]', dump)


def parse_headers(request):
    header_dump = re.findall(r'.*:.*[^\n]', request)
    headers = []
    for header in header_dump: 
        header = list(header)
        header.insert(0, '"')
        header.append('"')
        header.insert(header.index(':'), '"')
        header.insert(header.index(':') + 2, '"')
        headers.append(''.join(header))
    
    return ast.literal_eval('{' + ','.join(headers) + '}')

print(parse_headers(a))