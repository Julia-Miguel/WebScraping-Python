# André Lucas Santos e Júlia Roberta Gomes Miguel

import requests
from bs4 import BeautifulSoup

urls = [
    'https://pt.wikipedia.org/wiki/O_Auto_da_Compadecida_(filme)',
    'https://pt.wikipedia.org/wiki/Raiders_of_the_Lost_Ark#Pr%C3%AAmios_e_nomea%C3%A7%C3%B5es',
    'https://pt.wikipedia.org/wiki/Ben-Hur',
    'https://pt.wikipedia.org/wiki/Titanic_(filme_de_1997)#Pr%C3%AAmios'
]

while True:
    print("\nFilmes disponíveis:\n")
        
    print("1.  O Auto da Compadecida")
    print("2.  Raiders of the Lost Ark")
    print("3.  Ben-Hur")
    print("4.  Titanic")

    choice = int(input("\nPor favor, escolha um filme pelo número: ")) - 1

    if 0 <= choice < len(urls):
        url = urls[choice]
    else:
        print("Escolha inválida.")
        exit(1)

    response = requests.get(url)

    if response.status_code == 200:
        content = response.text

        soup = BeautifulSoup(content, 'html.parser')

        table = soup.find('table', class_=['infobox_v2', 'infobox'])
        
        def get_enredo():
            try:
                enredo_element = soup.find("span", {"id": "Enredo"})
                if enredo_element:
                    enredo_paragraph = enredo_element.find_next("p")
                    for ref in enredo_paragraph.find_all('sup'):
                        ref.decompose()
                    return enredo_paragraph.text.strip()
                else:
                    return "Enredo não disponível"
            except Exception as e:
                print(f"Erro ao obter enredo: {e}")
                return "Enredo não disponível"

        def get_premios():
            try:
                premios_element = soup.find("span", {"id": "Prêmios_e_indicações"}) or \
                                soup.find("span", {"id": "Prêmios"}) or \
                                soup.find("span", {"id": "Prêmios_e_nomeações"})
                if premios_element:
                    premios_list = premios_element.find_next("p")
                    for ref in premios_list.find_all('sup'):
                        ref.decompose()
                    return premios_list.text.strip()
                else:
                    return "Prêmios não disponíveis"
            except Exception as e:
                print(f"Erro ao obter prêmios: {e}")
                return "Prêmios não disponíveis"

        if table:
            genre_found = False
            cast_found = False
            music_found = False
            release_found = False
            title_found = False
            title = table.find('th', class_='topo cinema')
            if title:
                title_found = True
                print("\n###########")
                print("Título encontrado:")
                print(title.get_text(strip=True))
                print("\n###########")
                print("Enredo:")
                print(get_enredo())
                print("\n###########")
                print("Prêmios:")
                print(get_premios())
            for row in table.find_all('tr'):
                header = row.find(['th', 'td'])
                if header:
                    header_text = header.get_text(strip=True)
                    if "Gênero" in header_text:
                        genre_found = True
                        print("\n###########")
                        print("Gêneros encontrados:")
                        for link in row.find_all('td')[1].find_all('a'):
                            print(link.get_text(strip=True))
                    elif "Elenco" in header_text:
                        cast_found = True
                        print("\n###########")
                        print("Elenco encontrado:")
                        for link in row.find_all('td')[1].find_all('a'):
                            print(link.get_text(strip=True))
                    elif "Música" in header_text:
                        music_found = True
                        print("\n###########")
                        print("Música encontrada:")
                        print(row.find_all('td')[1].get_text(strip=True))
                    elif "Lançamento" in header_text:
                        release_found = True
                        print("\n###########")
                        print("Data de lançamento encontrada:")
                        print(row.find_all('td')[1].get_text(strip=True).replace('[1]', ''))
            
            if not genre_found:
                print("Cabeçalho 'Gênero' não encontrado.")
            if not cast_found:
                print("Cabeçalho 'Elenco' não encontrado.")
            if not music_found:
                print("Cabeçalho 'Música' não encontrado.")
            if not release_found:
                print("Cabeçalho 'Lançamento' não encontrado.")
            if not title_found:
                print("Cabeçalho do título não encontrado.")
        else:
            print("Nenhuma tabela encontrada.")
    else:
        print("Falha ao obter a página.")
    again = input("\nDeseja escolher outro filme? (s/n): ")
    if again.lower() != 's':
        break