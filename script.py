#####Smetanin Eduard
#####test task for CTS trade
import requests
from bs4 import BeautifulSoup

URL = "https://www.cts-tradeit.cz/kariera/"


#Make get request to recive html.
def get_html(url):
    r = requests.get(url)
    return r


#Working with html object, and create files.
def get_professions_names(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('a', class_="card card-lg card-link-bottom")
    professions = []
    links = []
    for item in items:
        professions.append({item.find('h3', class_='card-title mb-0').text.strip()})
        links.append({item.get('href')})
    print('Active positions on CTS wep page:')
    print(professions)
    #print('Chcete vypsat podrobnsti do txt? formatu?\n'+'Press Y for write everything to the file')
    user_answer = 'y'
    if user_answer == 'y':
        for link in links:
            link_to_page = URL + repr(link).replace('/kariera/','').replace('{','').replace('}','').replace("'","")
            soup_two = BeautifulSoup(get_html(link_to_page).text, 'html.parser')
            professions_items = soup_two.find_all('div', class_="content")
            profession_inf = []
            for item in professions_items:
                profession_inf.append({
                    'Profession name': item.find('h1', class_='mb-1').text.strip(),
                    'Profession description': item.find('div', class_='container-9 mb-md-5').text.strip(),
                    'Job address': item.find('a', class_='text-gray').text.strip(),
                    'What to wait on this position': item.find('div', class_='story__text').text.strip(),
                    'Benefits': item.find('div', class_='row row-lg').text.strip()

                })
                f = open(item.find('h1', class_='mb-1').text.strip().replace('/',' ')+'.txt', "a")
                f.write(item.find('div', class_='story__text').text.strip())
                f.close

                for my_tag in soup_two.find_all(class_="list-check"):
                    profession_inf.append({
                        'What we need and what we offer': my_tag.text.strip()
                    })
                    #print(my_tag.text)
            print(profession_inf)
            print(link_to_page)


#Calling function to make get request
def parse():
    html = get_html(URL)
    if html.status_code == 200:
        get_professions_names(html.text)
    else:
        print("Error")


def main():
    parse()


if __name__ == "__main__":
    main()