from datetime import datetime
from time import sleep

from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from MargoBot.BotKlasy.postac_class import Postac


def pobierz_czas():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time


class BotE2(Postac):

    def __init__(self, login, haslo, nick):
        super().__init__(login, haslo, nick)
        self.czekaj_na_e2 = WebDriverWait(self.driver, 2000)

    def atakuj_e2(self, id_e2):
        try:
            if self.driver.find_element(By.ID, id_e2).is_enabled():
                self.driver.find_element(By.ID, id_e2).click()
                sleep(0.7)
        except:
            pass

    def usun_komunikat(self):
        try:
            if self.driver.find_element(By.ID, "alert").is_displayed():
                self.driver.find_element(By.ID, "a_ok").click()
        except:
            pass

    def elita_ubita(self, id_e2):
        try:
            if self.driver.find_element(By.ID, id_e2).is_displayed() and not(self.driver.find_element(By.ID, "battle").is_displayed()):
                return False
            else:
                return True
        except StaleElementReferenceException:
            return False
        except NoSuchElementException:
            return True

    def anty_afk(self):
        self.driver.implicitly_wait(5)
        sleep(2)
        kordy = self.pobierz_kordy_postaci()
        while kordy == self.pobierz_kordy_postaci():
            self.ruch_gora()
        while kordy != self.pobierz_kordy_postaci():
            self.ruch_dol()

    def bij_e2(self, id_e2, czas, kordy, kordy_mapy):
        licznik = 0
        self.czekaj_na_e2.until(expected_conditions.visibility_of_element_located((By.ID, id_e2)))
        print("Start", pobierz_czas())
        while True:
            self.atakuj_e2(id_e2)
            self.usun_komunikat()
            if self.elita_ubita(id_e2):
                sleep(2)
                if self.driver.find_element(By.ID, "battle").is_displayed():
                    licznik += 1
                    print(f"Złapałeś E2 po raz: {licznik}    {pobierz_czas()}")
                    self.przejdz_walke()
                else:
                    print(f"Ktoś ubił: {pobierz_czas()}")
                self.usun_komunikat()
                self.dojdz_na_kordy(kordy, kordy_mapy)
                sleep(czas)
                self.odswiez_gre()
                self.anty_afk()
                self.czekaj_na_e2.until(expected_conditions.visibility_of_element_located((By.ID, id_e2)))

    def stoj_kolo_e2(self, id_e2, czas):
        licznik = 0
        self.czekaj_na_e2.until(expected_conditions.visibility_of_element_located((By.ID, id_e2)))
        print("Start", pobierz_czas())
        while True:
            if self.elita_ubita(id_e2):
                sleep(2)
                if self.driver.find_element(By.ID, "battle").is_displayed():
                    licznik += 1
                    print(f"Ubiłeś E2 po raz: {licznik}    {pobierz_czas()}")
                    self.przejdz_walke()
                else:
                    print(f"Ktoś ubił: {pobierz_czas()}")
                self.usun_komunikat()
                sleep(czas)
                self.odswiez_gre()
                self.anty_afk()
                self.czekaj_na_e2.until(expected_conditions.visibility_of_element_located((By.ID, id_e2)))
