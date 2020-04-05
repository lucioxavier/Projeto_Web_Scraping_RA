#Importando as bibliotecas mais importantes
from time import sleep
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC # Importar classe para ajudar a localizar os elementos
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

problems_links = []
problems_links_2 = []
links = []

#Definição - Funções de estilização
def titulo_in():
    titulo_ = 'WEBSCRAPING - RECLAME AQUI'
    print('='*40)
    print(f'{titulo_:^40}')
    print('='*40)

def linha_div():
    print('-'*40)

#Definição - Função de interação com o usuário
def def_operadora():
    global pag_in, qtd_pag, operadora, url_in, url_fin
    linha_div()
    pag_in = int(input('Digite a página que deseja iniciar: '))
    qtd_pag = int(input('Digite a quantidade de páginas desejadas: '))
    operadora = str(input('Digite a operadora que deseja pesquisar: ')).upper().strip()
    url_in = f'https://www.reclameaqui.com.br'
    url_tim = f'/empresa/tim-celular/lista-reclamacoes/?pagina='
    url_vivo = f'/empresa/vivo-celular-fixo-internet-tv/lista-reclamacoes/?pagina='
    url_claro = f'/empresa/claro/lista-reclamacoes/?pagina='
    url_oi = f'/empresa/oi-movel-fixo-tv/lista-reclamacoes/?pagina='
    if operadora in 'TIM':
        linha_div()
        url_fin = f'{url_in}{url_tim}'
    elif operadora in 'VIVO':
        linha_div()
        url_fin = f'{url_in}{url_vivo}'
        linha_div()
    elif operadora in 'CLARO':
        linha_div()
        url_fin = f'{url_in}{url_claro}'
    elif operadora in 'OI':
        linha_div()
        url_fin = f'{url_in}{url_oi}'
    else:
        linha_div()
        print(f'Você não selecionou uma operadora elegível!\nExecute o código novamente.')

#Defnição - Funções de execução
def abrir_navegador():
    global chrome, wait
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument('--ignore-ssl-errors')
    chrome = webdriver.Chrome(executable_path='C:\PYTHON\chromedriver', chrome_options=options)
    wait = WebDriverWait(chrome, 4)
    linha_div()
    print('Navegador aberto...')

def carregando_url(url_):
    global ra_page
    button_path = '//*[@id="brand-page-controller"]/div[4]/div[2]/div[2]/div[2]/div/div[3]/div[3]/div[3]/ul/li[8]/a'
    elemento = False
    contador = 0
    while elemento is False:
        try:
            chrome.get(url_)
            chrome.implicitly_wait(4)
            elemento = wait.until(EC.element_to_be_clickable((By.XPATH, button_path)))
        except:
            contador +=33
            sleep(2)
            print(f'Tentando carregar página novamente... {contador}%')
            if contador > 100:
                problems_links.append(url_)
                print('Página não carregada... Link adicionado aos problems_links.')
                break
        else:
            print('Página carregada com sucesso!')
            ra_page = bs(chrome.page_source, 'html.parser')
            sleep(4)
            elemento = True

def carregando_url_2(url_2):
    global ra_page_2
    button_path_2 = '//*[@id="complain-detail"]/div/div[2]/div/div[1]'
    elemento_2 = False
    contador_2 = 0
    while elemento_2 is False:
        try:
            chrome.get(url_2)
            chrome.implicitly_wait(4)
            elemento_2 = wait.until(EC.element_to_be_clickable((By.XPATH, button_path_2)))
        except:
            contador_2 +=33
            sleep(2)
            print(f'Tentando carregar página novamente... {contador_2}%')
            if contador_2 > 100:
                problems_links_2.append(url_2)
                print('Página não carregada... Link adicionado aos problems_links.')
                break
        else:
            print('Página carregada com sucesso!') 
            ra_page_2 = bs(chrome.page_source, 'html.parser')
            sleep(4)
            elemento_2 = True

def criando_arq():
    with open(f'reclame_aqui_{operadora}.csv', 'w') as _file:
        _file.write('Titulo_reclamacao; Empresa; Local; ID_reclamacao; Data; Hora; Descricao\n') 

titulo_in()
def_operadora()
criando_arq()
abrir_navegador()

for page in range(pag_in, qtd_pag+1):
    carregando_url(f'{url_fin}{page}')
    boxes = ra_page.find('div', {'class': 'content-loader'})
    sleep(4)

    for c, box in enumerate(boxes.find_all('a')):
        links.append(box.get('href'))
        print(f'Salvando link ({c+1}/{len(boxes)})')
        sleep(2)

    linha_div()
    print('Iniciando processo de acesso aos links...')
    linha_div()
    for link in links:
        carregando_url_2(f'{url_in}{link}')
        selection_1 = ra_page_2.find('div', {'class': 'col-md-10 col-sm-12'})
        selection_2 = selection_1.find('ul')
        titulo = selection_1.find('h1').text.strip()
        empresa = selection_1.find('p').text.strip()
        local = selection_2.find('li', {'class':'ng-binding'}).text.strip()
        id_ = selection_2.find('li', {'class':'ng-scope'}).text.strip()
        data = selection_2.find_all('li', {'class':'ng-binding'})[1].text[0:9].strip()
        hora = selection_2.find_all('li', {'class':'ng-binding'})[1].text[-5:].strip()
        descricao = ra_page_2.find('div', {'class':'complain-body'}).text.strip()
        l = [titulo, empresa, local, id_, data, hora, descricao]
        with open(f'reclame_aqui.{operadora}csv', 'a') as _file2:
            _file2.write(f'{l[0]};{l[1]};{l[2]};{l[3]};{l[4]};{l[5]};{l[6]}\n')
        l.clear()
        sleep(4)
    links.clear()
    print(f'Todos links deste bloco carregados.')

chrome.quit()
