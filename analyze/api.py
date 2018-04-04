import requests
from bs4 import BeautifulSoup


def jukuu(word):
    params = {
        'q': word
    }
    res = requests.get('http://www.jukuu.com/search.php', params=params)
    soup = BeautifulSoup(res.text, 'html.parser')

    for c, e in zip(soup.find_all('tr', {'class':'c'}), soup.find_all('tr', {'class':'e'})):
        yield {
            'Chinese': c.text.strip(),
            'English': e.text.strip()
        }


if __name__ == '__main__':
    print(list(jukuu('寒假')))
