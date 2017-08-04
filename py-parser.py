import urllib.request
import urllib.parse
import os
import webbrowser
import http.client
from threading import Thread

""" Um parser em python usando threads e http client para fazer requisicao no site
    retornando o body da pagina
"""

# Variavel global para receber os dados em bytes do parse na url
global __response_data
__response_data = None

# Inicia o script
def init():

    arquivo = None
    path_to_save = None


    host = input("Digite a url que deseja fazer o parse > http://")

    # Formata a url
    full_url = "http://{}".format(host)

    # Retorna o status da requisicao no site inserido
    # Retorna False se requisicao falhou
    # Retorna um objeto HTTPResponse
    reponse = get_response(full_url)

    # Se o response retorna false entao termina o script
    if not reponse:
        return

    # Cria uma Thread para rodar em background o parse da url
    background_request = Thread(target=parse_request, args=(full_url, reponse, ))
    background_request.start()

    # Pega o nome do site formato em string
    url_name = host.split('.')[0]

    # Reebe nome para salvar o arquivo, default e a url_name
    new_url_name = input("Digite o nome do arquivo [default: {}] > ".format(url_name))

    if new_url_name != "":
        url_name = new_url_name

    status = False
    while status is False:
        try:

            # Recebe o lugar para salvar o arquivo
            path_to_save = save_path()

            # Enquanto o parse nao esta carregado, mostra mensagem carregado
            show_once = 0
            while __response_data is None:
                if show_once == 0:
                    print ("** Carregando **")
                show_once += 1

            # Cria o arquivo html ou sobrescreve em um ja existente
            arquivo = open("{}/{}.html".format(path_to_save, url_name), "w")

            # Printa no arquivo criado os dados do parse da url
            arquivo.write(__response_data.decode('utf-8'))
            arquivo.close()

            status = True

        except IOError as erro:
            print(erro)
        finally:
            if arquivo is not None:
                arquivo.close()

    # Recebe a escolha se quiser abrir o arquivo no navegador
    choice = input("Deseja abrir o site no navegador? [Y/n] > ")
    choice_options = (choice == 'y') or (choice == 'Y') or (choice == 'Yes') or (choice == 'YES')

    # Se choice_options for true entao abre o arquivo no navegador
    if choice_options:
        path = os.path.abspath(arquivo.name)
        webbrowser.open("file://" + path, new=0)

def save_path():
    """ Funcao que retorna o diretorio para salvar o arquivo """

    path_to_save = None

    while path_to_save is None:
        print ("Digite aonde deseja salvar o arquivo >")
        path_to_save = input()

        if not os.path.isdir(path_to_save):
            print ("O diretorio informado nao e um diretorio ou nao existe.")
            print ("Tente novamente.")
            path_to_save = None
    return path_to_save

def parse_request(url, response):
    """ Faz o parse na url atribuindo a variavel global __response_data os dados
        retornados da requisicao
    """

    global __response_data

    try:
        __response_data = response.read()
    except (ConnectionError, urllib.request.HTTPError, urllib.request.URLError) as erro:
        print (erro)
    finally:
        response.close()

def get_response(url):
    """ Verifica se a url inserida e valida, se nao for printa a mensagem de erro
        e retorna False
    """

    try:
        print ("** Carregando **")

        return urllib.request.urlopen(url)
    except (ConnectionError, urllib.request.HTTPError, urllib.request.URLError) as erro:
        print ("Erro: {}" .format(erro))
        return False

# Inicia o script
if (__name__ == '__main__'):
    init()
