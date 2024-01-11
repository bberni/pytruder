import colorama


def create_row(number, payload, code, time, length, index):
    #funkcja odpowiedzialna za ładne wyświetlanie danych otrzymanych z serwera
    if index % 2 == 0:
        row = f"|{number.rjust(20)} |{payload.rjust(20)} |{code.rjust(20)} |{time.rjust(20)} |{length.rjust(20)} |"
    else:
        row = (
            "|"
            + f"{number.rjust(20)} |{payload.rjust(20)} |{code.rjust(20)} |{time.rjust(20)} |{length.rjust(20)} "
            + colorama.Style.RESET_ALL
            + "|"
        ) 
    return row


def print_border():
    print(f'+{"-" * 109}+')
