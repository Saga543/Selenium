from time import sleep
# from datetime import datetime
from selenium import webdriver
# from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, \
    StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from pynput.keyboard import Controller, Key


keyboard = Controller()
driver = webdriver.Chrome(ChromeDriverManager().install())
actions = webdriver.ActionChains(driver)
wait5 = WebDriverWait(driver, 5, 0.5)
wait10 = WebDriverWait(driver, 10, 0.5)
wait30 = WebDriverWait(driver, 30, 0.5)


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
        wait10.until(expected_conditions.visibility_of_element_located((By.ID, "panel")))
        wait10.until(expected_conditions.visibility_of_element_located((By.ID, 'bchat')))
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
        # ZainstalujDodatki()
    except:
        UruchomGre(login, haslo, postacXpath)


def CzyElementJestDostepny(element, typ):
    obiekt = None
    try:
        if typ == "id":
            obiekt = driver.find_element(By.ID, element)
        elif typ == "css":
            obiekt = driver.find_element(By.CSS_SELECTOR, element)
        elif typ == "classname":
            obiekt = driver.find_element(By.CLASS_NAME, element)
        else:
            print("Nieprawidłowy typ")
        if obiekt.is_displayed():
            print("Dostępny")
            return True
        else:
            print("Jest na mapie, ale nie wyświetlony")
            return False
    except NoSuchElementException:
        print("Nie ma")
        return False


def PobierzKordyPostaci():  # 1,1  11,11   1,11    11,1  x = [0] y = [1]
    try:
        kordyText = driver.find_element(By.ID, "botloc").text
        kordyPostaci = []
        if len(kordyText) == 5:
            kordyPostaci = [int(kordyText[0] + kordyText[1]), int(kordyText[3] + kordyText[4])]
        elif len(kordyText) == 3:
            kordyPostaci = [int(kordyText[0]), int(kordyText[2])]
        elif len(kordyText) == 4:
            if kordyText[1] == ",":
                kordyPostaci = [int(kordyText[0]), int(kordyText[2] + kordyText[3])]
            elif kordyText[2] == ",":
                kordyPostaci = [int(kordyText[0] + kordyText[1]), int(kordyText[3])]
        else:
            print("Nie udało się pobrać kordynatów")
        return kordyPostaci
    except:
        PobierzKordyPostaci()


def RuszSie(kierunek: str):
    ruchyPostaci = {"prawo": [505, 280], "lewo": [10, 280], "gora": [280, 10], "dol": [280, 505],
                    "prawoGora": [505, 15], "prawoDol": [505, 505], "lewoGora": [15, 15], "lewoDol": [15, 505]}
    if kierunek in ruchyPostaci.keys():
        ruch = ruchyPostaci.get(kierunek)
        x = ruch[0]
        y = ruch[1]
        ground = driver.find_element(By.ID, "bground")
        actions.move_to_element_with_offset(ground, x, y).click().perform()
    else:
        print("Zła nazwa kierunku")


def UsunKomunikat():
    try:
        driver.find_element(By.ID, "a_ok").click()
        return True
    except Exception:
        return False


def CzyJestesObokNpc(kordy: []):
    postacKordy = PobierzKordyPostaci()
    x = postacKordy[0]
    y = postacKordy[1]
    if (x in range(kordy[0] - 1, kordy[0] + 2)) and (y in range(kordy[1] - 1, kordy[1] + 2)):
        print("Jesteś obok npc")
        return True
    else:
        return False


def PobierzMape():
    wait5.until(expected_conditions.visibility_of_element_located((By.ID, "botloc")))
    mapa = driver.find_element(By.ID, "botloc")
    lokalizacja = mapa.get_attribute("tip")
    # print(lokalizacja)
    return lokalizacja

# plik = open("mapy.txt", "w")
# mapy = []
# while len(mapy) < 10:
#     mapa = PobierzMape()
#     if not mapa in mapy:
#         mapy.append(mapa)
# plik.write(str(mapy))
# plik.close()

# def DojdzNaMape(cel: str):
#     lokalizacja = PobierzMape()
#     print(lokalizacja)
#     przejscie = driver.find_element(By.ID, "gw16175")
#     DojdzDoNpc(przejscie, [47, 63])
# try:
#     przejscie = driver.find_element(By.ID, "gw43")
#     DojdzDoNpc(przejscie, [43, 0])
#     sleep(5)
#     przejscie = driver.find_element(By.ID, "gw47")
#     DojdzDoNpc(przejscie, [47, 0])
#
# except:
#     pass

def DojdzDoNpc(npc, kordy: []):  # ID npc i jego kordy
    ruch = ""
    while not CzyJestesObokNpc(kordy):
        postacKordy = PobierzKordyPostaci()
        x = postacKordy[0]
        y = postacKordy[1]
        if npc.is_displayed():
            npc.click()
        if npc.is_displayed() is False:
            if (x < kordy[0]) and (y >= kordy[1]):
                ruch = "prawoGora"
            elif (x <= kordy[0]) and (y < kordy[1]):
                ruch = "prawoDol"
            elif (x >= kordy[0]) and (y > kordy[1]):
                ruch = "lewoGora"
            elif (x > kordy[0]) and (y <= kordy[1]):
                ruch = "lewoDol"
            else:
                print("Coś nie tak")
                continue
        RuszSie(ruch)
        sleep(2.5)


def ZamknijWalke():
    wait5.until(expected_conditions.visibility_of_element_located((By.ID, "battle")))
    oknoWalki = driver.find_element(By.ID, "battle")
    if oknoWalki.is_displayed():
        zamknijWalke = driver.find_element(By.ID, "battleclose")
        potwierdzLot = driver.find_element(By.ID, "loots_button")
        wait10.until(expected_conditions.visibility_of_element_located((By.ID, "autobattleButton")))
        driver.find_element(By.ID, "autobattleButton").click()
        wait10.until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "win")))
        if CzyElementJestDostepny("win", 'classname'):
            zamknijWalke.click()
        if potwierdzLot.is_displayed():
            potwierdzLot.click()


def PrzejdzWalke():
    try:
        if driver.find_element(By.ID, "battle").is_displayed():
            if driver.find_element(By.ID, "autobattleButton").is_displayed():
                driver.find_element(By.ID, "autobattleButton").click()
            if driver.find_element(By.ID, "loots_button").is_displayed():
                driver.find_element(By.ID, "loots_button").click()
            if CzyElementJestDostepny("win", 'classname'):
                sleep(0.5)
                if driver.find_element(By.ID, "battleclose").is_displayed():
                    driver.find_element(By.ID, "battleclose").click()
    except ElementClickInterceptedException or ElementNotInteractableException or StaleElementReferenceException:
        PrzejdzWalke()


def BijPotwory(sciezka: {}):
    for potwor in sciezka:
        try:
            cel = driver.find_element(By.ID, potwor)
        except NoSuchElementException:
            continue
        DojdzDoNpc(cel, sciezka.get(potwor))
        while CzyJestesObokNpc(sciezka.get(potwor)) is False:
            if CzyJestesObokNpc(sciezka.get(potwor)):
                cel.click()
                sleep(0.5)
                PrzejdzWalke()


def AntyKonsola():
    try:
        if driver.find_element(By.XPATH, "//*[@id='contxt']").is_displayed():
            driver.refresh()
            wait5.until(expected_conditions.invisibility_of_element_located((By.XPATH, "//*[@id='contxt']")))
        else:
            return True
    except:
        AntyKonsola()


def JakasFunkcja():
    pola = [[26, 61], [26, 60], [26, 59], [26, 58], [26, 57], [26, 56], [26, 55], [26, 54], [26, 53], [26, 52],
            [26, 51],
            [26, 50], [27, 50], [28, 50], [29, 50], [30, 50], [31, 50], [32, 50], [33, 50], [34, 50], [35, 50],
            [36, 50], [37, 50], [37, 49], [37, 48], [37, 47], [37, 46], [37, 45], [37, 44], [37, 43], [37, 42],
            [37, 41],
            [37, 40], [37, 39], [37, 38], [36, 38], [35, 38], [34, 38], [33, 38], [32, 38], [31, 38], [30, 38],
            [29, 38],
            [28, 38], [27, 38], [26, 38], [26, 37], [26, 36], [26, 35], [26, 34], [25, 34], [24, 34], [23, 34],
            [23, 33],
            [23, 32], [23, 31], [23, 30], [23, 29], [23, 28], [23, 27], [23, 26], [23, 25], [23, 24], [23, 23],
            [23, 22],
            [23, 21], [23, 20], [22, 20], [21, 20], [20, 20], [19, 20], [18, 20], [17, 20], [17, 19], [17, 18],
            [17, 17],
            [16, 17], [15, 17], [14, 17], [13, 17], [12, 17], [12, 16], [12, 15], [12, 14], [12, 13], [12, 12],
            [12, 11],
            [12, 10], [11, 10], [10, 10], [9, 10], [9, 9], [9, 8], [9, 7], [8, 7], [7, 7], [6, 7], [5, 7], [4, 7]]
    pola2 = []
    while PobierzMape() == "Karka-han":
        kordy = PobierzKordyPostaci()
        if not kordy in pola2:
            pola2.append(kordy)
    print(pola2)

    for nextStep in pola:
        kordy = PobierzKordyPostaci()
        x = kordy[0]
        y = kordy[1]
        if y > nextStep[1]:
            RuchGora()
        elif y < nextStep[1]:
            RuchDol()
        elif x < nextStep[0]:
            RuchPrawo()
        elif x > nextStep[0]:
            RuchLewo()

def RuchPrawo():
    keyboard.press(Key.right)
    sleep(0.25)
    keyboard.release(Key.right)


def RuchLewo():
    keyboard.press(Key.left)
    sleep(0.25)
    keyboard.release(Key.left)


def RuchGora():
    keyboard.press(Key.up)
    sleep(0.25)
    keyboard.release(Key.up)


def RuchDol():
    keyboard.press(Key.down)
    sleep(0.25)
    keyboard.release(Key.down)


def odswiez_gre():
    try:
        driver.refresh()
        sleep(3)
        if driver.find_element(By.ID, "loading").is_displayed():
            odswiez_gre()
    except:
        odswiez_gre()


UruchomGre("kuba92800", "b0l0ssec0m", "//div[@data-nick = 'Rithuru']")
while True:
    driver.execute_script("changeClient()")
    sleep(5)


