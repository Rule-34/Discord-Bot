from config import debug


# Prints if debug is true
def debug_print(text):
    if debug:
        print('\n %s' % (text))
