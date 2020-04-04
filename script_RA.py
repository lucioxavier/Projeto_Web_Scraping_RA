#Importando as bibliotecas mais importantes
from time import sleep
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC # Importar classe para ajudar a localizar os elementos
from selenium.webdriver.common.by import By

links = []
l = []




def titulo_in():
    titulo_ = 'WEBSCRAPING - RECLAME AQUI'
    print('='*40)
    print(f'{titulo_:^40}')
    print('='*40)

def linha_div():
    print('-'*40)

def def_operadora():
    linha_div()
    operadora = str(input('Digite a operadora que deseja pesquisar: ')).upper().strip()
    global url_in
    url_in = f'https://www.reclameaqui.com.br'
    url_tim = f'/empresa/tim-celular/lista-reclamacoes/?pagina='
    url_vivo = f'/empresa/vivo-celular-fixo-internet-tv/lista-reclamacoes/?pagina='
    url_claro = f'/empresa/claro/lista-reclamacoes/?pagina='
    url_oi = f'/empresa/oi-movel-fixo-tv/lista-reclamacoes/?pagina='
    global url_fin
    if operadora in 'TIM':
        url_fin = f'{url_in}{url_tim}'
    elif operadora in 'VIVO':
        url_fin = f'{url_in}{url_vivo}'
    elif operadora in 'CLARO':
        url_fin = f'{url_in}{url_claro}'
    elif operadora in 'OI':
        url_fin = f'{url_in}{url_oi}'
    else:
        print(f'Você não selecionou uma operadora elegível!')

def abrir_navegador():
    global chrome, wait
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument('--ignore-ssl-errors')
    chrome = webdriver.Chrome(executable_path='C:\PYTHON\chromedriver', chrome_options=options)
    wait = WebDriverWait(chrome, 1)
    print('Navegador aberto...')

def carregando_url(url_):
    chrome.get(url_)
    print('Carregando a página...')
    sleep(4)

def criando_arq():
    with open('reclame_aqui.csv', 'w') as _file:
        _file.write('Titulo_reclamacao; Empresa; Local; ID_reclamacao; Data; Hora; Descricao\n') 

titulo_in()
qtd_pag = int(input('Digite a quantidade de páginas desejadas: '))
linha_div()
criando_arq()
def_operadora()
abrir_navegador()

for c in range(1, qtd_pag+1):
    carregando_url(f'{url_fin}{c}')
    ra_page = bs(chrome.page_source, 'html.parser')
    sleep(4)
    boxes = ra_page.find('div', {'class': 'content-loader'})
    sleep(4)

    for c, box in enumerate(boxes.find_all('a')):
        links.append(box.get('href'))
        print(f'Salvando link ({c+1}/{len(boxes)})')
        sleep(2)

    print('acessando links')
    for link in links:
        recarregar = False
        contador = 0
        while recarregar is False:
            try:
                carregando_url(f'{url_in}{link}')
                ra_page2 = bs(chrome.page_source, 'html.parser')
                selection_1 = ra_page2.find('div', {'class': 'col-md-10 col-sm-12'})
                selection_2 = selection_1.find('ul')
            except:
                contador += 3
                sleep(3)
                print(f'Tentando novamente... {contador}')
                if contador > 100:
                    break
                else:
                    print(f'Aguarde...{contador}')
                    sleep(2)
            else:
                print('Página carregada com sucesso...')
                break
        
        titulo = selection_1.find('h1').text.strip()
        empresa = selection_1.find('p').text.strip()
        local = selection_2.find('li', {'class':'ng-binding'}).text.strip()
        id_ = selection_2.find('li', {'class':'ng-scope'}).text.strip()
        data = selection_2.find_all('li', {'class':'ng-binding'})[1].text[0:9].strip()
        hora = selection_2.find_all('li', {'class':'ng-binding'})[1].text[-5:].strip()
        descricao = ra_page2.find('div', {'class':'complain-body'}).text.strip()
        l = [titulo, empresa, local, id_, data, hora, descricao]
        with open('reclame_aqui.csv', 'a') as _file2:
            _file2.write(f'{l[0]};{l[1]};{l[2]};{l[3]};{l[4]};{l[5]};{l[6]}\n')
        l.clear()
        sleep(4)
        contador = 0
    links.clear()
    print(f'carregou todas deste bloco')

chrome.quit()
