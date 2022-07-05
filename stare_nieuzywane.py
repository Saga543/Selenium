def PobierzKordyPostaci():  # 1,1  11,11   1,11    11,1  x = [0] y = [1]
    try:
        kordyText = driver.find_element(By.ID, "botloc").text
        kordy = []
        if not kordyText:
            PobierzKordyPostaci()
        elif kordyText:
            if len(kordyText) == 5:
                kordy = [int(kordyText[0] + kordyText[1]), int(kordyText[3] + kordyText[4])]
            elif len(kordyText) == 3:
                kordy = [int(kordyText[0]), int(kordyText[2])]
            elif len(kordyText) == 4:
                if kordyText[1] == ",":
                    kordy = [int(kordyText[0]), int(kordyText[2] + kordyText[3])]
                elif kordyText[2] == ",":
                    kordy = [int(kordyText[0] + kordyText[1]), int(kordyText[3])]
            else:
                print("Nie udało się pobrać kordynatów")
        if len(kordy) == 0:
            return PobierzKordyPostaci()
        else:
            return kordy
    except:
        return PobierzKordyPostaci()


def AtakujE2(idE2):
    if CzyElementJestDostepny(idE2, "id"):
        e2 = driver.find_element(By.ID, idE2)
        sleep(1)
        while CzyElementJestDostepny("battle", "id") is False:
            e2.click()
            sleep(1.5)
            if CzyElementJestDostepny("battle", "id"):
                ZamknijWalke()
                WrocNaMiejsce(54, 55, 38, 42)
                sleep(2)
                WyjdzNaChwile(120)
                break

# try:
        #     element = driver.find_element(By.ID, msgLista[i])
        #     napisy.append(element)
        #     if element.is_displayed():
        #         element.click()
        #     continue
        # except NoSuchElementException:
        #     continue

def CzyElementIstniejeID(element):
    driver.implicitly_wait(5)
    try:
        driver.find_element(By.ID, element)
        print("Jest")
        return True
    except NoSuchElementException:
        print("Nie ma")
        return False


def CzyElementJestWyswietlony(element):
    driver.implicitly_wait(5)
    element = driver.find_element(By.ID, element)
    if element.is_displayed():
        print("Wyświetlony")
        return True
    else:
        print("Niewyświetlony")
        return False


def Dialog3():
    wait.until(expected_conditions.visibility_of_element_located((By.ID, "npc178362")))
    anisja = driver.find_element(By.ID, "npc178362")
    odpowiedz = driver.find_element(By.ID, "replies")
    meliorn = driver.find_element(By.ID, "npc178365")
    anisja.click()
    sleep(3)
    anisja.click()
    odpowiedz.click()
    wait.until(expected_conditions.visibility_of_element_located((By.ID, "replies")))
    odpowiedz.click()
    wait.until(expected_conditions.visibility_of_element_located((By.ID, "npc178365")))
    meliorn.click()
    sleep(3)
    meliorn.click()
    odpowiedz.click()
    odpowiedz.click()

def PrzejdzDialog2():
    ground = driver.find_element(By.ID, "bground")
    renard = driver.find_element(By.ID, "npc178339")
    pajak = driver.find_element(By.ID, "npc178348")
    odpowiedz = driver.find_element(By.ID, "replies")
    renard.click()
    wait.until(expected_conditions.visibility_of_element_located((By.ID, "replies")))
    odpowiedz.click()
    sleep(0.5)
    actions.move_to_element_with_offset(ground, 128, 256).click().perform()
    sleep(1)
    pajak.click()
    sleep(2)
    pajak.click()
    sleep(2)
    driver.find_element(By.ID, "battleclose").click()
    sleep(0.5)
    actions.move_to_element_with_offset(ground, 384, 280).double_click().perform()
    sleep(1)
    if renard.is_displayed():
        renard.click()
    else:
        actions.move_to_element_with_offset(ground, 384, 256).click().perform()
        renard.click()
    sleep(2)
    renard.click()
    wait.until(expected_conditions.visibility_of_element_located((By.ID, "replies")))
    odpowiedz.click()
    sleep(0.5)
    wait.until(expected_conditions.visibility_of_element_located((By.XPATH, "//*[@id='replies'']")))
    odpowiedz.click()
    actions.move_to_element_with_offset(ground, 128, 256).click().perform()
    sleep(1.5)
    driver.find_element(By.ID, "npc178358").click()  # wyjście
    sleep(1.5)
    driver.find_element(By.ID, "npc178358").click()
    sleep(3)

def PrzejdzDialog1():
    renard = driver.find_element(By.ID, "npc178339")
    odpowiedz = driver.find_element(By.ID, "replies")
    renard.click()
    sleep(1)
    renard.click()
    wait.until(expected_conditions.visibility_of_element_located((By.ID, "replies")))
    odpowiedz.click()
    sleep(0.5)
    odpowiedz.click()
    sleep(0.5)

def IdzDoNpc(npcCel, NPC: []):  # npc i jego kordy
    postacKordy = PobierzKordyPostaci()
    print(postacKordy)
    if npcCel.is_displayed():
        npcCel.click()                    #range pomija drugi argument
        if (postacKordy[0] in range(NPC[0] - 1, NPC[0] + 1)) and (postacKordy[1] in range(NPC[1] - 1, NPC[1] + 1)):
            print("Jesteś obok postaci")
        else:
            print("Jesteś za daleko od postaci")
            npcCel.click()
    elif npcCel.is_displayed() == False:
        pass

def ZalozEQ1():
    sleep(0.5)
    bron = driver.find_element(By.XPATH, "//img[@src='https://micc.garmory-cdn.cloud/obrazki/itemy/roz/rozdzka08.gif']")
    pomka = driver.find_element(By.XPATH, "//img[@src='https://micc.garmory-cdn.cloud/obrazki/itemy/orb/orb08.gif']")
    EQ = driver.find_element(By.ID, "panel")
    sleep(1)
    actions.click_and_hold(bron).move_to_element_with_offset(EQ, 70, 160).release().perform()
    sleep(1)
    actions.click_and_hold(pomka).move_to_element_with_offset(EQ, 70, 160).release().perform()
    sleep(0.5)

def DojdzDoNpc(npc, kordy: []):  # ID npc i jego kordy
    ruch = ""
    znaleziony = False
    while True:
        postacKordy = PobierzKordyPostaci()
        x = postacKordy[0]
        y = postacKordy[1]
        if npc.is_displayed():
            if not znaleziony:
                npc.click()
                znaleziony = True
            break
        elif npc.is_displayed() is False:
            if (x in range(kordy[0] - 1, kordy[0] + 2)) and (y > kordy[1]):
                ruch = "gora"
            elif (x in range(kordy[0] - 1, kordy[0] + 2)) and (y < kordy[1]):
                ruch = "dol"
            elif (x < kordy[0]) and (y in range(kordy[1] - 1, kordy[1] + 2)):
                ruch = "prawo"
            elif (x > kordy[0]) and (y in range(kordy[1] - 1, kordy[1] + 2)):
                ruch = "lewo"
            elif (x < kordy[0]) and (y >= kordy[1] + 2):
                ruch = "prawoGora"
            elif (x < kordy[0]) and (y <= kordy[1] - 2):
                ruch = "prawoDol"
            elif (x > kordy[0]) and (y >= kordy[1] + 2):
                ruch = "lewoGora"
            elif (x > kordy[0]) and (y <= kordy[1] - 2):
                ruch = "lewoDol"
            else:
                print("Coś nie tak")
                continue
        RuszSie(ruch)
        sleep(1)