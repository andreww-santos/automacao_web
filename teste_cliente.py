import random
from faker import Faker
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pytest
import time

class TestCliente:
    # Definindo seletores como constantes
    SELETOR_CONTA = ".mb-3:nth-child(1) .form-control"
    SELETOR_USUARIO = ".mb-3:nth-child(2) .form-control"
    SELETOR_SENHA = ".mb-0:nth-child(1)"
    SELETOR_ENTRAR = "button.btn.btn-primary.w-100.btn-dark"
    SELETOR_ICON_CARTAO = ".fa-address-card"
    SELETOR_SUBMENU_CADASTROS = ".submenu ul span.item-label"
    SELETOR_SUBMENU_CLIENTES = ".submenu ul span.item-title"
    SELETOR_LINK_CLIENTES = "a[href='/clientes/gerenciar-clientes/pesquisa']"
    SELETOR_CNPJ = ".col-sm-6 .input-group > .form-control"
    SELETOR_NOME_CLIENTE = ".row:nth-child(3) > .col-xs-12:nth-child(1) > .mb-3 > .form-control"
    SELETOR_NOME_FANTASIA = "div[name='fantasia'] input[name='fantasia']"  # Seletor para Nome Fantasia
    SELETOR_DATA_NASCIMENTO = "input[name='dt_nascto']"  # Seletor para Data de Nascimento
    SELETOR_EMAIL = "div[name='email'] input[name='email']"  # Seletor para o campo e-mail
    SELETOR_TELEFONE = "div[name='fone'] input[name='fone']"  # Seletor para o campo telefone
    SELETOR_CEP = "div[name='cep'] input[name='cep']"  # Seletor para o campo CEP
    SELETOR_LOGRADOURO = "div[name='endereco'] input[name='endereco']"  # Seletor para o Logradouro
    SELETOR_NUMERO = "div[name='numero'] input[name='numero']"  # Seletor para o Número
    SELETOR_BAIRRO = "div[name='bairro'] input[name='bairro']"  # Seletor para o Bairro
    SELETOR_MUNICIPIO = "div[name='descricao_municipio'] input[name='descricao_municipio']"  # Seletor para o Município
    SELETOR_UF = "div[name='uf'] input[name='uf']"  # Seletor para o UF
    SELETOR_BOTAO_SALVAR = "button.btn.btn-primary"  # Corrigido para o botão de salvar
    SELETOR_BOTAO_NOVO = "button.btn.btn-success"

    def setup_method(self):
        self.fake = Faker()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.maximize_window()

    def teardown_method(self):
        self.driver.quit()

    def espera_carregador_desaparecer(self):
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located((By.ID, "main-loader"))
        )

    def gerar_cnpj(self):
        cnpj = [random.randint(0, 9) for _ in range(12)]
        cnpj_str = ''.join(map(str, cnpj))
        return f'{cnpj_str[:2]}.{cnpj_str[2:5]}.{cnpj_str[5:8]}/{cnpj_str[8:12]}-{random.randint(10, 99)}'

    def gerar_telefone(self):
        # Gera um número de telefone brasileiro
        ddd = random.randint(11, 99)  # DDD aleatório
        numero = random.randint(10000000, 99999999)  # Número aleatório
        return f'({ddd}) {numero}'

    def gerar_data_nascimento(self):
        # Gera uma data de nascimento aleatória para uma pessoa entre 18 e 65 anos
        data_nascimento = self.fake.date_of_birth(minimum_age=18, maximum_age=65)
        return data_nascimento.strftime('%d/%m/%Y')

    def gerar_cep(self):
        # Gera um CEP aleatório no formato XXXXX-XXX
        cep = f"{random.randint(10000, 99999)}-{random.randint(100, 999)}"
        return cep

    def gerar_logradouro(self):
        # Gera um logradouro aleatório
        return self.fake.street_address()

    def gerar_numero(self):
        # Gera um número aleatório entre 1 e 999
        return random.randint(1, 999)

    def gerar_bairro(self):
        # Gera um bairro aleatório
        return self.fake.city()

    def scroll_para_baixo(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)  # Pausa para garantir que a rolagem seja realizada

    def test_cadcliente(self):
        conta_fixa = "andreteste"
        usuario_fixo = "andre"
        senha_fixa = "123"

        # Geração de dados aleatórios
        cnpj_aleatorio = self.gerar_cnpj()
        nome_cliente = self.fake.company()
        nome_fantasia = self.fake.company_suffix() + " " + self.fake.bs().capitalize()  # Nome Fantasia
        data_nascimento = self.gerar_data_nascimento()  # Data de nascimento aleatória
        email_aleatorio = self.fake.email()  # Gera um e-mail aleatório
        telefone_aleatorio = self.gerar_telefone()  # Gera um telefone aleatório
        cep_aleatorio = self.gerar_cep()  # Gera um CEP aleatório
        logradouro_aleatorio = self.gerar_logradouro()  # Gera um logradouro aleatório
        numero_aleatorio = self.gerar_numero()  # Gera um número entre 1 e 999
        bairro_aleatorio = self.gerar_bairro()  # Gera um bairro aleatório
        municipio_aleatorio = self.fake.city()  # Gera um município aleatório

        self.driver.get("https://deploy.bruningsistemas.com.br/login")

        try:
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".nome-usuario"))
            )
            print("Usuário já está logado. Pulando login.")
            return
        except:
            print("Usuário não está logado. Prosseguindo com o login.")

        self.espera_carregador_desaparecer()

        try:
            # Preenchendo os campos de login
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, self.SELETOR_CONTA))
            ).send_keys(conta_fixa)
            self.scroll_para_baixo()  # Rolagem após inserir o campo de conta

            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, self.SELETOR_USUARIO))
            ).send_keys(usuario_fixo)
            self.scroll_para_baixo()  # Rolagem após inserir o campo de usuário

            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, self.SELETOR_SENHA))
            ).send_keys(senha_fixa)
            self.scroll_para_baixo()  # Rolagem após inserir o campo de senha

            entrar_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, self.SELETOR_ENTRAR))
            )
            self.driver.execute_script("arguments[0].click();", entrar_button)

            self.espera_carregador_desaparecer()

            # Navegação até o menu de cadastro de clientes
            icon_cartao = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, self.SELETOR_ICON_CARTAO))
            )
            ActionChains(self.driver).move_to_element(icon_cartao).perform()

            submenu_cadastros = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, self.SELETOR_SUBMENU_CADASTROS))
            )
            ActionChains(self.driver).move_to_element(submenu_cadastros).perform()

            submenu_clientes = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, self.SELETOR_SUBMENU_CLIENTES))
            )
            ActionChains(self.driver).move_to_element(submenu_clientes).perform()

            # Clica no link "Clientes"
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, self.SELETOR_LINK_CLIENTES))
            ).click()

            self.espera_carregador_desaparecer()

            # Clica no botão "Novo"
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, self.SELETOR_BOTAO_NOVO))
            ).click()

            # Preenche o campo CNPJ
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, self.SELETOR_CNPJ))
            ).send_keys(cnpj_aleatorio)
            self.scroll_para_baixo()  # Rolagem após inserir o CNPJ

            # Preenche o campo Nome do Cliente
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, self.SELETOR_NOME_CLIENTE))
            ).send_keys(nome_cliente)
            self.scroll_para_baixo()  # Rolagem após inserir o Nome do Cliente

            # Preenche o campo Nome Fantasia
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, self.SELETOR_NOME_FANTASIA))
            ).send_keys(nome_fantasia)
            self.scroll_para_baixo()  # Rolagem após inserir o Nome Fantasia

            # Preenche o campo Data de Nascimento
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, self.SELETOR_DATA_NASCIMENTO))
            ).send_keys(data_nascimento)
            self.scroll_para_baixo()  # Rolagem após inserir a Data de Nascimento

            # Preenche o campo E-mail
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, self.SELETOR_EMAIL))
            ).send_keys(email_aleatorio)
            self.scroll_para_baixo()  # Rolagem após inserir o E-mail

            # Preenche o campo Telefone
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, self.SELETOR_TELEFONE))
            ).send_keys(telefone_aleatorio)
            self.scroll_para_baixo()  # Rolagem após inserir o Telefone

            # Preenche o campo CEP
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, self.SELETOR_CEP))
            ).send_keys(cep_aleatorio)
            self.scroll_para_baixo()  # Rolagem após inserir o CEP

            # Aguardar que o carregador desapareça
            self.espera_carregador_desaparecer()

            # Preenche o campo Logradouro
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, self.SELETOR_LOGRADOURO))
            ).send_keys(logradouro_aleatorio)
            self.scroll_para_baixo()  # Rolagem após inserir o Logradouro

            # Preenche o campo Número
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, self.SELETOR_NUMERO))
            ).send_keys(numero_aleatorio)
            self.scroll_para_baixo()  # Rolagem após inserir o Número

            # Preenche o campo Bairro
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, self.SELETOR_BAIRRO))
            ).send_keys(bairro_aleatorio)
            self.scroll_para_baixo()  # Rolagem após inserir o Bairro

            # Preenche o campo Município (autocomplete)
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, self.SELETOR_MUNICIPIO))
            ).send_keys(municipio_aleatorio)
            self.scroll_para_baixo()  # Rolagem após inserir o Município
            
            time.sleep(1)  # Espera para que as sugestões carreguem

            # Seleciona o primeiro item da lista de sugestões
            lista_municipios = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".data-list-options"))
            )
            primeiro_municipio = lista_municipios.find_element(By.TAG_NAME, 'li')
            primeiro_municipio.click()

            # Aguardar que o carregador desapareça
            self.espera_carregador_desaparecer()

            # Clica no botão "Salvar"
            submit_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, self.SELETOR_BOTAO_SALVAR))
            )
            submit_button.click()

            # Verifica se a URL mudou para a de pesquisa
            WebDriverWait(self.driver, 10).until(EC.url_contains("/clientes/gerenciar-clientes/pesquisa"))
            print("Cliente cadastrado com sucesso.")

        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            assert False  # Caso ocorra erro, falha o teste
