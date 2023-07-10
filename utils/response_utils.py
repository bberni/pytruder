import requests

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