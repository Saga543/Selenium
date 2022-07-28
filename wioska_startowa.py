from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
#from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver import Firefox


# Dane do logowania
login = ""
haslo = ""

driver = Firefox(executable_path=GeckoDriverManager().install())
driver.get('https://www.margonem.pl/profile/view,5722142#char_1120398,tarhuna')
driver.maximize_window()
wait = WebDriverWait(driver, 40, 0.5)
actions = webdriver.ActionChains(driver)


def Zaloguj(login, haslo):
    driver.find_element(By.ID, "login-input").send_keys(login)
    driver.find_element(By.ID, "login-password").send_keys(haslo)
    driver.find_element(By.ID, "js-login-btn").click()
    wait.until(expected_conditions.visibility_of_element_located(
        (By.XPATH, "/html/body/div[3]/div/div[1]/div/div[2]/div[4]/div/div")))
    driver.find_element(By.XPATH, "/html/body/div[3]/div/div[1]/div/div[2]/div[4]/div/div").click()
    sleep(3)
    RozwinChat()


def RozwinChat():
    wait.until(expected_conditions.visibility_of_element_located((By.ID, 'bchat')))
    driver.find_element(By.ID, 'bchat').click()
    driver.find_element(By.ID, 'bchat').click()
    driver.find_element(By.ID, 'bchat').click()


def Quest1():
    renard = driver.find_element(By.ID, "npc178339")
    odpowiedz = driver.find_element(By.ID, "replies")
    pajak = driver.find_element(By.ID, "npc178348")
    wyjscie = driver.find_element(By.ID, "npc178358")
    kordyPostaci = {renard: [17, 15], pajak: [7, 14], wyjscie: [7, 20]}
    kolejnosc = [renard, renard, odpowiedz, odpowiedz, renard, odpowiedz, pajak, pajak, renard, renard,
                 odpowiedz, odpowiedz, wyjscie, wyjscie]
    i = 0
    while i < len(kolejnosc):
        cel = kolejnosc[i]
        if i == 4:
            ZalozItemy()
        if CzyElementJestDostepny(cel, "id"):
            kolejnosc[1].click()
        elif CzyElementJestDostepny(cel, "id") is False:
            # DojdzDoNpc(cel)
            pass


def OtworzSzkatulke():
    szkatulka = driver.find_element(By.ID, "item32716221")
    actions.double_click(szkatulka).perform()


# wykonuje ruch w wyznaczonym kierunku
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


# zwraca kordy postaci
def PobierzKordyPostaci():  # 1,1  11,11   1,11    11,1  x = [0] y = [1]
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


def DojdzDoNpc(npc, kordy: []):  # ID npc i jego kordy
    while True:
        postacKordy = PobierzKordyPostaci()
        x = postacKordy[0]
        y = postacKordy[1]
        if npc.is_displayed():
            if (x in range(kordy[0] - 1, kordy[0] + 1)) and (y in range(kordy[1] - 1, kordy[1] + 1)):
                print("Jesteś obok npc")
                return True
            else:
                npc.click()
        elif npc.is_displayed() is False:
            if (x >= kordy[0] - 4) and (x <= kordy[0] - 4) and (y > kordy[1]):
                RuszSie("gora")
            elif (x >= kordy[0] - 4) and (x <= kordy[0] - 4) and (y < kordy[1]):
                RuszSie("dol")
            elif (x < kordy[0]) and (y >= kordy[1] - 4) and (y <= kordy[1] + 4):
                RuszSie("prawo")
            elif (x > kordy[0]) and (y >= kordy[1] - 4) and (y <= kordy[1] + 4):
                RuszSie("lewo")
            elif (x < kordy[0]) and (y >= kordy[1] + 4):
                RuszSie("prawoGora")
            elif (x < kordy[0]) and (y <= kordy[1] - 4):
                RuszSie("prawoDol")
            elif (x > kordy[0]) and (y >= kordy[1] + 4):
                RuszSie("lewoGora")
            elif (x > kordy[0]) and (y <= kordy[1] - 4):
                RuszSie("lewoDol")
            else:
                print("Coś nie tak")
                continue
        sleep(1)


# zwraca true jeśli item istnieje na mapie i jest widoczny, przyjmuje element, str typ elementu
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


def UsunZolteNapisy():
    msgLista = ['msg0', 'msg1', 'msg2', 'msg3', 'msg4', 'msg5', 'msg6', 'msg7', 'msg8', 'msg9', 'msg10']
    napisy = []
    sleep(0.5)
    i = 0
    while i < len(msgLista):
        if CzyElementJestDostepny(msgLista[i], "id"):  #do poprawy
            element = driver.find_element(By.ID, msgLista[i])
            napisy.append(element)
            element.click()
            continue
        else:
            continue
    print(len(napisy))


# zwraca lokalizację postaci
def PobierzMape():
    wait.until(expected_conditions.visibility_of_element_located((By.ID, "botloc")))
    mapa = driver.find_element(By.ID, "botloc")
    lokalizacja = mapa.get_attribute("tip")
    print(lokalizacja)
    return lokalizacja


#przyjmuje jeden lub kilka elementów i przeciąga na EQ
def ZalozItemy(*args):
    EQ = driver.find_element(By.ID, "panel")
    for item in args:
        actions.click_and_hold(item).move_to_element_with_offset(EQ, 70, 160).release().perform()
        sleep(0.5)


# zwraca liste itemów na 1 lvl
def Itemylvl1():
    rozdzka = driver.find_element(By.XPATH,
                                  "//img[@src='https://micc.garmory-cdn.cloud/obrazki/itemy/roz/rozdzka08.gif']")
    orb = driver.find_element(By.XPATH, "//img[@src='https://micc.garmory-cdn.cloud/obrazki/itemy/orb/orb08.gif']")
    listaItemow = [rozdzka, orb]
    return listaItemow


def ZamknijWalke():
    if CzyElementJestDostepny("battle", "id"):
        zamknijWalke = driver.find_element(By.ID, "battleclose")
        potwierdzLot = driver.find_element(By.ID, "loots_button")
        driver.find_element(By.ID, "autobattleButton").click()
        if CzyElementJestDostepny("win", 'classname'):
            zamknijWalke.click()
            sleep(0.5)
        if potwierdzLot.is_displayed():
            potwierdzLot.click()


def PrzejdzDialog():
    wait.until(expected_conditions.visibility_of_element_located((By.ID, "replies")))
    if CzyElementJestDostepny("replies", "id"):
        odpowiedz = driver.find_element(By.ID, "replies")
        odpowiedz.click()
        #UsunZolteNapisy() bug
        PrzejdzDialog()
    else:
        print("Koniec")


Zaloguj(login, haslo)

npc = driver.find_element(By.ID, "npc178365")
npc.click()
PrzejdzDialog()

# driver.execute_script()
# exp bot, połączyć potwory grafem, npc też można do grafu
