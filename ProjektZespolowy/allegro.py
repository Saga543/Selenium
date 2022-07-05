#from time import sleep
# from datetime import datetime
from selenium import webdriver
# from selenium.common.exceptions import NoSuchElementException
#from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
#from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


driver = webdriver.Chrome(ChromeDriverManager().install())
actions = webdriver.ActionChains(driver)
wait5 = WebDriverWait(driver, 5, 0.5)
wait10 = WebDriverWait(driver, 10, 0.5)
wait30 = WebDriverWait(driver, 30, 0.5)


def uruchom_allegro():
    driver.get("https://allegro.pl/")
    driver.maximize_window()
    driver.implicitly_wait(10)
    driver.find_element(By.XPATH, "//*[@id='opbox-gdpr-consents-modal']/div/div[2]/div[2]/button[1]").click()


def wyszukaj_oferty(przedmiot):
    wyszukiwarka_xpath = "/html/body/div[2]/div[3]/div/div/div/div/div/div[3]/header/div/div/div/div/form/input"
    driver.find_element(By.XPATH, wyszukiwarka_xpath).send_keys(przedmiot, Keys.ENTER)


def zwroc_liste_ofert():
    lista = driver.find_elements(By.XPATH, "//article[@data-analytics-enabled='true']")
    print(len(lista))
    return lista


def wypisz_oferty():
    oferty = zwroc_liste_ofert()
    for oferta in oferty:
        print(oferta.get_attribute("aria-label"))


def zbierz_ceny():
    oferty = zwroc_liste_ofert()
    lista_cen = []
    for oferta in oferty:
        cena = oferta.get_attribute("aria-label").split()
        print(cena)
        lista_cen.append(cena)
    print(lista_cen)


uruchom_allegro()
wyszukaj_oferty("laptop")
driver.implicitly_wait(10)
wypisz_oferty()
zbierz_ceny()

