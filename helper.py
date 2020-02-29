from config import debug


# Prints if debug is true
def debug_print(text):
    if debug:
        print('\n %s' % (text))


# Workaround since Twitter has banned creating favorites by API, so add them to the file and fav them manually
def log_to_file(text):
    with open("log.txt", "a") as log_file:
        log_file.write(text)
