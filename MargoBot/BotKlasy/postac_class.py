"""Klasa do wykonywania akcji postacią"""
from selenium.common.exceptions import ElementNotInteractableException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from MargoBot.BotKlasy.uruchom_gre_class import UruchomGre
from MargoBot.GrafBFS.bfs import zwroc_sciezke


class Postac(UruchomGre):

    def __init__(self, login, haslo, nick):
        super().__init__(login, haslo, nick)
        self.waitMapa = WebDriverWait(self.driver, 5, 0.01)

    def pobierz_mape(self):
        try:
            self.waitMapa.until(expected_conditions.visibility_of_element_located((By.ID, "botloc")))
            lokalizacja = self.driver.find_element(By.ID, "botloc").get_attribute("tip")
            if lokalizacja is None:
                return self.pobierz_mape()
            else:
                return lokalizacja
        except:
            return self.pobierz_mape()

    def pobierz_kordy_postaci(self):
        try:
            kordy = self.driver.find_element(By.ID, "botloc").text
            if kordy is None:
                return self.pobierz_kordy_postaci()
            kordy = kordy.split(",")
            return [int(kordy[0]), int(kordy[1])]
        except:
            return self.pobierz_kordy_postaci()

    def dojdz_na_kordy(self, docelowe_kordy, kordy_mapy):
        sciezka = zwroc_sciezke(self.pobierz_kordy_postaci(), docelowe_kordy, kordy_mapy)
        if sciezka is None:
            return False
        for nastepny_krok in sciezka:
            kordy = self.pobierz_kordy_postaci()
            if (kordy[0] == nastepny_krok[0]) and (kordy[1] > nastepny_krok[1]):
                while (kordy[0] == nastepny_krok[0]) and (kordy[1] > nastepny_krok[1]):
                    self.ruch_gora()
                    kordy = self.pobierz_kordy_postaci()
            elif (kordy[0] == nastepny_krok[0]) and (kordy[1] < nastepny_krok[1]):
                while (kordy[0] == nastepny_krok[0]) and (kordy[1] < nastepny_krok[1]):
                    self.ruch_dol()
                    kordy = self.pobierz_kordy_postaci()
            elif (kordy[0] < nastepny_krok[0]) and (kordy[1] == nastepny_krok[1]):
                while (kordy[0] < nastepny_krok[0]) and (kordy[1] == nastepny_krok[1]):
                    self.ruch_prawo()
                    kordy = self.pobierz_kordy_postaci()
            elif (kordy[0] > nastepny_krok[0]) and (kordy[1] == nastepny_krok[1]):
                while (kordy[0] > nastepny_krok[0]) and (kordy[1] == nastepny_krok[1]):
                    self.ruch_lewo()
                    kordy = self.pobierz_kordy_postaci()
        if self.pobierz_kordy_postaci() != docelowe_kordy:
            print("Powtórz")
            self.dojdz_na_kordy(docelowe_kordy, kordy_mapy)

    def wcisnij_auto(self):
        try:
            if self.driver.find_element(By.ID, "autobattleButton").is_displayed():
                self.driver.find_element(By.ID, "autobattleButton").click()
        except:
            self.wcisnij_auto()

    def ruch_prawo(self):
        self.driver.execute_script("hero.go(g.keys.arrows[39])")

    def ruch_lewo(self):
        self.driver.execute_script("hero.go(g.keys.arrows[37])")

    def ruch_gora(self):
        self.driver.execute_script("hero.go(g.keys.arrows[38])")

    def ruch_dol(self):
        self.driver.execute_script("hero.go(g.keys.arrows[40])")

    def przejdz_walke(self):
        try:
            self.wait10.until(expected_conditions.element_to_be_clickable((By.ID, "autobattleButton")))
        except TimeoutException:
            pass
        self.driver.execute_script("_g('fight&a=f')")
        try:
            self.wait10.until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "win")))
        except TimeoutException:
            pass
        self.driver.execute_script("canLeave()")
        if self.driver.find_element(By.ID, "loots_button").is_displayed():
            try:
                self.driver.find_element(By.ID, "loots_button").click()
            except ElementNotInteractableException:
                pass
