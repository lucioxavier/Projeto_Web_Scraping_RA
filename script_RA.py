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



