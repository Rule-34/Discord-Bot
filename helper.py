from config import debug


# Prints if debug is true
def debug_print(text):
    if debug:
        print('\n %s' % (text))


# Hardcoded max_count, would probably need to use a fetch
list_of_domains = [{'name': 'rule34.xxx', 'short': 'xxx', 'max_count': 3659351},
                   {'name': 'rule34.paheal.net',
                       'short': 'paheal', 'max_count': 3532797},
                   {'name': 'danbooru.donmai.us',
                       'short': 'danbooru', 'max_count': 3806415},
                   {'name': 'gelbooru.com', 'short': 'gelbooru', 'max_count': 5164061},
                   {'name': 'e621.net', 'short': 'e621', 'max_count': 2168016}]
