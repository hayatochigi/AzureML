def get_sub(path):
    file = open(path, 'r')
    sub = file.read()
    file.close()

    return sub