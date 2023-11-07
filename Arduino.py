from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def chamaArduino():

    # Crie uma instância do navegador
    driver = webdriver.Chrome()

    # Acesse a página pelo IP
    ip_address = "192.168.101.12/go"
    driver.get("http://" + ip_address)

    # Localize o elemento pelo ID "servo" e clique nele
    link_text = "motorservo"  # varíavel com o texto do hyperlink
    element = driver.find_element(By.LINK_TEXT, link_text)

    time.sleep(20)
    
    # clica
    element.click()

    # Feche o navegador
    driver.quit()
