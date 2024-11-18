def nfvHeaderWrite(program_txt):
    header = open("header.txt", "r")
    header_content = header.read()
    new_program = header_content + program_txt
    return new_program


def trafficConfigsValidator(data):
    if data["rate"] == 0:
        return 200
    else:
        return 404
