from bs4 import BeautifulSoup


def has_forbidden_content(text):
    if bool(BeautifulSoup(text, "html.parser").find()):
        return True

    if 'http' in text:
        return True