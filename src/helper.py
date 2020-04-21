from config import debug
from json import load as load_json


# -------- Init -------- #

# Hardcoded max_count, would probably need to use a fetch
with open('assets/lib/rule-34-shared-resources/domains.json', 'r') as json_data:
    list_of_domains = load_json(json_data)

    # Delete domains that we are not gonna use
    list_of_domains[:] = [
        d for d in list_of_domains if d.get('short') != 'loli']


# -------- Helper functions -------- #

# Returns dictionary with the domain
def find_domain_by_selector(domain, selector='short'):
    for domain_from_list in list_of_domains:
        if domain_from_list[selector] == domain:
            return domain_from_list

    # Return none if nothing is found
    return None


# Prints if debug is true
def debug_print(text):
    if debug:
        print('\n %s' % (text))


def invoqued_by(name, command=None):
    debug_print(f'{command}: invoqued by {name}')