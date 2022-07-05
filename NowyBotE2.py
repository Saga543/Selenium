from time import sleep
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver import Firefox


driver = Firefox(executable_path=GeckoDriverManager().install())
actions = webdriver.ActionChains(driver)
wait5 = WebDriverWait(driver, 5, 0.5)
wait10 = WebDriverWait(driver, 10, 0.5)
wait30 = WebDriverWait(driver, 30, 0.5)
czekajNaE2 = WebDriverWait(driver, 2000, 0.5)


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
        sleep(0.7)
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
       # ZainstalujDodatki()
    except:
        UruchomGre(login, haslo, postacXpath)


def PobierzKordyPostaci():  # 1,1  11,11   1,11    11,1  x = [0] y = [1]
    try:
        kordy = driver.find_element(By.ID, "botloc").text
        if kordy is None:
            PobierzKordyPostaci()
        kordy = kordy.split(",")
        return [int(kordy[0]), int(kordy[1])]
    except:
        return PobierzKordyPostaci()


def PobierzMape():
    wait5.until(expected_conditions.visibility_of_element_located((By.ID, "botloc")))
    mapa = driver.find_element(By.ID, "botloc")
    lokalizacja = mapa.get_attribute("tip")
    return lokalizacja


def PobierzCzas():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time


def ElementDostepnyClass(element):
    try:
        if driver.find_element(By.CLASS_NAME, element).is_displayed():
            return True
        else:
            return False
    except NoSuchElementException:
        return False


def ElementDostepnyID(element):
    try:
        if driver.find_element(By.ID, element).is_displayed():
            return True
        else:
            return False
    except NoSuchElementException:
        pass


def PrzejdzWalke():
    try:
        wait5.until(expected_conditions.visibility_of_element_located((By.ID, "battle")))
        if driver.find_element(By.ID, "battle").is_displayed():
            sleep(1)
            driver.find_element(By.ID, "autobattleButton").click()
            wait10.until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "win")))
            if ElementDostepnyClass("win"):
                driver.find_element(By.ID, "battleclose").click()
            if driver.find_element(By.ID, "loots_button").is_displayed():
                driver.find_element(By.ID, "loots_button").click()
    except:
        PrzejdzWalke()


def RuszSie2(kierunek: str):
    ruchyPostaci = {"prawo": [330, 280], "lewo": [220, 280], "gora": [256, 220], "dol": [256, 350],
                    "prawoGora": [330, 220], "prawoDol": [350, 350], "lewoGora": [220, 220], "lewoDol": [220, 350]}
    if kierunek in ruchyPostaci.keys():
        ruch = ruchyPostaci.get(kierunek)
        x = ruch[0]
        y = ruch[1]
        ground = driver.find_element(By.ID, "bground")
        actions.move_to_element_with_offset(ground, x, y).click().perform()
    else:
        print("Zła nazwa kierunku")


def WrocNaMiejsce(x1, x2, y1, y2):
    while True:
        try:
            postacKordy = PobierzKordyPostaci()
            x = postacKordy[0]
            y = postacKordy[1]
            if (x in range(x1, x2 + 1)) and (y in range(y1, y2 + 1)):
                # print("Wróciłeś na miejsce")
                break
            elif (x in range(x1, x2 + 1)) and (y > y2):
                RuszSie2("gora")
            elif (x in range(x1, x2 + 1)) and (y < y1):
                RuszSie2("dol")
            elif (x < x1) and (y in range(y1, y2 + 1)):
                RuszSie2("prawo")
            elif (x > x2) and (y in range(y1, y2 + 1)):
                RuszSie2("lewo")
            elif (x < x1) and (y > y2):
                RuszSie2("prawoGora")
            elif (x < x1) and (y < y1):
                RuszSie2("prawoDol")
            elif (x > x2) and (y > y2):
                RuszSie2("lewoGora")
            elif (x > x2) and (y < y1):
                RuszSie2("lewoDol")
            else:
                print("Coś nie tak")
            sleep(0.5)
        except:
            continue


def AntyAFK(x1, x2, y1, y2):
    try:
        actions.move_to_element_with_offset(driver.find_element(By.ID, "bground"), 256, 60).click().perform()
        sleep(1)
        WrocNaMiejsce(x1, x2, y1, y2)
    except:
        pass


def UsunKomunikat():
    try:
        if driver.find_element(By.ID, "alert").is_displayed():
            driver.find_element(By.ID, "a_ok").click()
    except:
        pass


def WrocNaMiejsceiCzekaj(e2ID, czas, x1, x2, y1, y2):
    sleep(1)
    WrocNaMiejsce(x1, x2, y1, y2)
    sleep(czas)
    OdswiezGre()
    AntyKonsola()
    AntyAFK(x1, x2, y1, y2)
    czekajNaE2.until(expected_conditions.visibility_of_element_located((By.ID, e2ID)))


def Atakuj(e2ID):
    try:
        if driver.find_element(By.ID, e2ID).is_enabled():
            driver.find_element(By.ID, e2ID).click()
            sleep(0.7)
    except:
        pass


def ElitaUbita(element):
    try:
        if driver.find_element(By.ID, element).is_displayed():
            return False
    except:
        return True


def AntyKonsola():
    try:
        if driver.find_element(By.XPATH, "//*[@id='contxt']").is_displayed():
            driver.refresh()
            wait5.until(expected_conditions.visibility_of_element_located((By.ID, "hero")))
    except:
        AntyKonsola()


def OdswiezGre():
    try:
        driver.refresh()
        driver.implicitly_wait(5)
    except:
        OdswiezGre()


def BotE2(e2ID, czas, x1, x2, y1, y2):
    licznik = 0
    czekajNaE2.until(expected_conditions.visibility_of_element_located((By.ID, e2ID)))
    print("Start", PobierzCzas())
    while True:
        AntyKonsola()
        Atakuj(e2ID)
        UsunKomunikat()
        if driver.find_element(By.ID, "battle").is_displayed():
            licznik += 1
            print("Złapałeś E2 po raz:", licznik, "  ", PobierzCzas())
            PrzejdzWalke()
            WrocNaMiejsceiCzekaj(e2ID, czas, x1, x2, y1, y2)
        elif ElitaUbita(e2ID):
            UsunKomunikat()
            print("Ktoś ubił", PobierzCzas())
            WrocNaMiejsceiCzekaj(e2ID, czas, x1, x2, y1, y2)


UruchomGre("kuba92800", "b0l0ssec0m", "//div[@data-nick = 'Rithuru']")
while True:
    OdswiezGre()
    sleep(2)
