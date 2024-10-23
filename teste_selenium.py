from selenium import webdriver

# Inicializa o Chrome WebDriver
driver = webdriver.Chrome()

# Acessa a página do Google
driver.get("https://www.google.com")

# Fechar o navegador após o uso
driver.quit()