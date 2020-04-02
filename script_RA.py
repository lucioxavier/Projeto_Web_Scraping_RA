#Importando as bibliotecas mais importantes
from time import sleep
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

#Definindo as variáveis mais importantes
url = f'https://www.reclameaqui.com.br/empresa/tim-celular/lista-reclamacoes/'
url_in = f'https://www.reclameaqui.com.br/empresa'
chrome = webdriver.Chrome(executable_path='C:\PYTHON\chromedriver')
wait = WebDriverWait(chrome, 0.1)
links = []
l = []

with open('reclame_aqui_TIM.csv', 'w') as _file:
    _file.write('Titulo_reclamacao; Empresa; Local; ID_reclamacao; Data; Hora; Descricao\n')


def carregando_url(urlx):
    chrome.get(urlx)

carregando_url(url)
sleep(2)
reclame_aqui_page = bs(chrome.page_source, 'html.parser')
conteiner = reclame_aqui_page.find('div', {'class': 'content-loader'})
for box in conteiner.find_all('a'):
    links.append(box.get('href'))

for link in links:
    carregando_url(f'{url_in}{link}')
    sleep(3)
    page = bs(chrome.page_source, 'html.parser')
    selection_1 = page.find('div', {'class': 'col-md-10 col-sm-12'})
    selection_2 = selection_1.find('ul')
    titulo = selection_1.find('h1').text.strip()
    empresa = selection_1.find('p').text.strip()
    local = selection_2.find('li', {'class':'ng-binding'}).text.strip()
    id_ = selection_2.find('li', {'class':'ng-scope'}).text.strip()
    data = selection_2.find_all('li', {'class':'ng-binding'})[1].text[0:9].strip()
    hora = selection_2.find_all('li', {'class':'ng-binding'})[1].text[-5:].strip()
    descricao = page.find('div', {'class':'complain-body'}).text.strip()
    lista_dados_temp = [titulo, empresa, local, id_, data, hora, descricao]
    l.append(lista_dados_temp[0:])
    lista_dados_temp.clear()

    with open('reclame_aqui_TIM.csv', 'a') as _file2:
        _file2.write(f'{l[0][0]};{l[0][1]};{l[0][2]};{l[0][3]};{l[0][4]};{l[0][5]};{l[0][6]}\n')
    l.clear()

chrome.quit()    


