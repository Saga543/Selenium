from datetime import datetime
from time import sleep
# from datetime import datetime
from selenium import webdriver
# from selenium.common.exceptions import NoSuchElementException
#from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from MargoBot.GrafBFS.bfs import zwroc_sciezke

driver = webdriver.Chrome(ChromeDriverManager().install())
actions = webdriver.ActionChains(driver)
wait5 = WebDriverWait(driver, 5, 0.5)
wait10 = WebDriverWait(driver, 10, 0.5)
wait30 = WebDriverWait(driver, 30, 0.5)
czekajNaE2 = WebDriverWait(driver, 900, 0.5)
waitMapa = WebDriverWait(driver, 5, 0.01)


def Zaloguj(login, haslo, xpathPostaci):
    driver.find_element(By.XPATH, "//*[@id='login-input']").send_keys(login)
    driver.find_element(By.ID, "login-password").send_keys(haslo)
    driver.find_element(By.ID, "js-login-btn").click()
    wait30.until(expected_conditions.visibility_of_element_located(
        (By.XPATH, "/html/body/div[3]/div/div[1]/div/div[2]/div[4]/div/div")))
    ZmienPostac(xpathPostaci)
    driver.find_element(By.XPATH, "/html/body/div[3]/div/div[1]/div/div[2]/div[4]/div/div").click()


def RozwinChat():
    try:
        wait30.until(expected_conditions.visibility_of_element_located((By.ID, 'bchat')))
        driver.find_element(By.XPATH, "//*[@id='bchat']").click()
        driver.find_element(By.XPATH, "//*[@id='bchat']").click()
        driver.find_element(By.XPATH, "//*[@id='bchat']").click()
    except:
        RozwinChat()


def ZmienPostac(xpathPostaci):
    driver.find_element(By.CLASS_NAME, "select-char").click()
    driver.find_element(By.XPATH, xpathPostaci).click()


def ZmienNaStaryInterface():
    try:
        wait5.until(expected_conditions.visibility_of_element_located((By.XPATH, "/html/body/div")))
        wait30.until(expected_conditions.visibility_of_element_located(
            (By.XPATH, "/html/body/div/div[4]/div[7]/div[3]/div[2]/div[10]")))
        driver.find_element(By.XPATH, "/html/body/div/div[4]/div[7]/div[3]/div[2]/div[10]").click()
        driver.find_element(By.CSS_SELECTOR,
                            "body > div > div.alerts-layer.layer > div.border-window.ui-draggable.window-on-peak > div.content > div.inner-content > div > div.bottom-bar > div.options-config-buttons.save-card-button > div.button.green.small.change-interface-btn > div.label").click()
        wait30.until(expected_conditions.visibility_of_element_located((By.ID, "panel")))
    except:
        pass


def ZainstalujDodatki():
    dodatki = {"filtr": "//*[@id='addon_114899']/div[2]/h2", "leczenie": "//*[@id='addon_3637']/div[2]/h2",
               "minutnik": "//*[@id='addon_21993']/div[2]/h2"}
    driver.find_element(By.ID, "b_addons").click()
    for nazwaDodatku in dodatki:
        driver.find_element(By.ID, "addon_search").send_keys(nazwaDodatku)
        driver.implicitly_wait(10)
        sleep(0.5)
        driver.find_element(By.XPATH, dodatki.get(nazwaDodatku)).click()
        driver.implicitly_wait(10)
        driver.find_element(By.XPATH, "//*[@id='addonDetails']/div/div[2]/div[3]/span[1]").click()
        sleep(0.5)
        driver.find_element(By.XPATH, "//*[@id='addonDetails']/div/div[2]/div[3]/span[2]").click()
        driver.find_element(By.ID, "addon_search").clear()
    driver.refresh()


def UruchomGre(login, haslo, postacXpath):
    try:
        driver.get('https://www.margonem.pl/profile/view,5722142#char_1120398,tarhuna')
        driver.maximize_window()
        Zaloguj(login, haslo, postacXpath)
        ZmienNaStaryInterface()
        RozwinChat()
        #ZainstalujDodatki()
    except:
        UruchomGre(login, haslo, postacXpath)


def PobierzMape():
    try:
        waitMapa.until(expected_conditions.visibility_of_element_located((By.ID, "botloc")))
        lokalizacja = driver.find_element(By.ID, "botloc").get_attribute("tip")
        if lokalizacja is None:
            return PobierzMape()
        else:
            return lokalizacja
    except:
        return PobierzMape()


def pobierz_kordy_postaci():  # 1,1  11,11   1,11    11,1  x = [0] y = [1]
    try:
        kordy = driver.find_element(By.ID, "botloc").text
        if kordy is None:
            pobierz_kordy_postaci()
        kordy = kordy.split(",")
        return [int(kordy[0]), int(kordy[1])]
    except:
        return pobierz_kordy_postaci()


def ruch_prawo():
    driver.execute_script("hero.go(g.keys.arrows[39])")
    driver.execute_script("hero.go(g.keys.arrows[39])")


def ruch_lewo():
    driver.execute_script("hero.go(g.keys.arrows[37])")
    driver.execute_script("hero.go(g.keys.arrows[37])")


def ruch_gora():
    driver.execute_script("hero.go(g.keys.arrows[38])")
    driver.execute_script("hero.go(g.keys.arrows[38])")


def ruch_dol():
    driver.execute_script("hero.go(g.keys.arrows[40])")
    driver.execute_script("hero.go(g.keys.arrows[40])")


def dojdz_na_kordy(docelowe_kordy, kordy_mapy):
    sciezka = zwroc_sciezke(pobierz_kordy_postaci(), docelowe_kordy, kordy_mapy)
    if sciezka is None:
        return False
    for nastepny_krok in sciezka:
        kordy = pobierz_kordy_postaci()
        x = kordy[0]
        y = kordy[1]
        if (x == nastepny_krok[0]) and (y > nastepny_krok[1]):
            while (x == nastepny_krok[0]) and (y > nastepny_krok[1]):
                ruch_gora()
                kordy = pobierz_kordy_postaci()
                x = kordy[0]
                y = kordy[1]
        elif (x == nastepny_krok[0]) and (y < nastepny_krok[1]):
            while (x == nastepny_krok[0]) and (y < nastepny_krok[1]):
                ruch_dol()
                kordy = pobierz_kordy_postaci()
                x = kordy[0]
                y = kordy[1]
        elif (x < nastepny_krok[0]) and (y == nastepny_krok[1]):
            while (x < nastepny_krok[0]) and (y == nastepny_krok[1]):
                ruch_prawo()
                kordy = pobierz_kordy_postaci()
                x = kordy[0]
                y = kordy[1]
        elif (x > nastepny_krok[0]) and (y == nastepny_krok[1]):
            while (x > nastepny_krok[0]) and (y == nastepny_krok[1]):
                ruch_lewo()
                kordy = pobierz_kordy_postaci()
                x = kordy[0]
                y = kordy[1]
    if pobierz_kordy_postaci() != docelowe_kordy:
        dojdz_na_kordy(docelowe_kordy, kordy_mapy)


def PobierzCzas():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time


UruchomGre("tomson321123", "kkkkk444", "//div[@data-nick = 'Grukar']")


pola2 = []
try:
    while PobierzMape() == "Namiot Vari Krugera":
        kordy = pobierz_kordy_postaci()
        if kordy not in pola2:
            pola2.append(kordy)
except:
    pass
pola2.sort()
plik = open("kordy.txt", "w")
plik.write(str(pola2))
plik.close()

